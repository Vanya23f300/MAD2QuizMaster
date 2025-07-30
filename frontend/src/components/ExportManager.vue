<template>
  <div class="export-manager">
    <!-- Export Status -->
    <div v-if="exportStatus" class="export-status mb-4">
      <div class="alert" :class="getStatusClass()">
        <div class="d-flex align-items-center">
          <div class="me-3">
            <i class="bi" :class="getStatusIcon()"></i>
          </div>
          <div class="flex-grow-1">
            <h5 class="alert-heading mb-1">{{ getStatusTitle() }}</h5>
            <p class="mb-0">{{ exportStatus.status }}</p>
            
            <!-- Authentication error -->
            <div v-if="isAuthError()" class="mt-2">
              <button class="btn btn-outline-light btn-sm" @click="redirectToLogin">
                <i class="bi bi-box-arrow-in-right me-1"></i>
                Log in again
              </button>
            </div>
          </div>
          <div v-if="exportStatus.state === 'completed'" class="ms-3">
            <button 
              class="btn btn-primary btn-sm"
              @click="downloadExport"
              :disabled="downloading"
            >
              <i class="bi bi-download me-2"></i>
              {{ downloading ? 'Downloading...' : 'Download' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Export Description -->
    <div class="export-description mb-4">
      <div class="card glass p-3">
        <h6 class="text-light mb-2">CSV Export Format</h6>
        <p class="text-light mb-2 small">
          The exported CSV file includes the following information for each quiz you've taken:
        </p>
        <div class="table-responsive">
          <table class="table table-sm table-dark small">
            <thead>
              <tr>
                <th>Field</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Quiz ID</td>
                <td>Unique identifier for the quiz</td>
              </tr>
              <tr>
                <td>Quiz Name</td>
                <td>Title of the quiz</td>
              </tr>
              <tr>
                <td>Chapter ID</td>
                <td>Unique identifier for the chapter</td>
              </tr>
              <tr>
                <td>Chapter Name</td>
                <td>Name of the chapter</td>
              </tr>
              <tr>
                <td>Subject ID</td>
                <td>Unique identifier for the subject</td>
              </tr>
              <tr>
                <td>Subject Name</td>
                <td>Name of the subject</td>
              </tr>
              <tr>
                <td>Date of Quiz</td>
                <td>Original date when quiz was created</td>
              </tr>
              <tr>
                <td>Attempt Date</td>
                <td>Date and time when you took the quiz</td>
              </tr>
              <tr>
                <td>Score</td>
                <td>Your score on the quiz</td>
              </tr>
              <tr>
                <td>Total Score</td>
                <td>Maximum possible score</td>
              </tr>
              <tr>
                <td>Percentage</td>
                <td>Your score as a percentage</td>
              </tr>
              <tr>
                <td>Passed</td>
                <td>Whether you passed the quiz</td>
              </tr>
              <tr>
                <td>Time Taken</td>
                <td>Time spent completing the quiz</td>
              </tr>
              <tr>
                <td>Remarks</td>
                <td>Additional notes about the quiz</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Export Options -->
    <div class="export-options">
      <h5 class="text-light mb-3">Export Quiz Data</h5>
      <p class="text-muted mb-4">
        Download your quiz history and performance data in CSV format.
        This will trigger a background job that may take a few moments to complete.
        You'll receive a notification when your export is ready to download.
      </p>

      <div class="d-grid">
        <button 
          class="btn btn-primary"
          @click="startExport"
          :disabled="loading || exportInProgress"
        >
          <span v-if="loading || exportInProgress">
            <i class="bi bi-arrow-repeat spin me-2"></i>
            {{ loading ? 'Starting Export...' : 'Export in Progress...' }}
          </span>
          <span v-else>
            <i class="bi bi-file-earmark-arrow-down me-2"></i>
            Export Quiz Data
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import ExportService from '@/services/export-service'
import notificationService from '@/services/notification-service'

export default {
  name: 'ExportManager',
  data() {
    return {
      loading: false,
      downloading: false,
      exportStatus: null,
      statusCheckInterval: null,
      currentTaskId: null,
      currentFilename: null
    }
  },
  computed: {
    exportInProgress() {
      return this.exportStatus && 
             ['pending', 'in_progress'].includes(this.exportStatus.state)
    }
  },
  methods: {
    async startExport() {
      this.loading = true;
      this.exportStatus = {
        state: 'pending',
        status: 'Preparing export request...'
      };
      
      try {
        console.log('🚀 Starting quiz export...');
        
        if (!ExportService || typeof ExportService.startExport !== 'function') {
          console.error('❌ Export service not properly initialized');
          throw new Error('Export service not available. Please try refreshing the page.');
        }
        
        // Log the token for debugging
        const token = localStorage.getItem('token');
        console.log('📝 Using authentication token:', token ? 'Valid token exists' : 'No token!');
        
        // Use the ExportService to start the export
        const result = await ExportService.startExport();
        
        console.log('✅ Export result:', result);
        
        if (result.success && result.data) {
          this.currentTaskId = result.data.task_id;
          this.currentFilename = result.data.filename;
          
          // Start checking status
          this.checkExportStatus();
          
          // Start periodic status checks
          this.statusCheckInterval = setInterval(this.checkExportStatus, 2000);
        } else {
          throw new Error(result.message || 'Failed to start export');
        }
      } catch (error) {
        console.error('❌ Export start error:', error);
        
        // Show a more detailed error message
        let errorMessage = 'Failed to start export. ';
        
        if (error.response) {
          // Server responded with an error status
          errorMessage += `Server responded with: ${error.response.status} ${error.response.statusText}`;
          console.error('Error details:', error.response.data);
        } else if (error.request) {
          // Request was made but no response received
          errorMessage += 'No response received from server. Please check if the backend is running.';
        } else {
          // Error in setting up the request or processing
          errorMessage += error.message || 'Unknown error occurred';
        }
        
        this.$emit('error', errorMessage);
        
        this.exportStatus = {
          state: 'failed',
          status: errorMessage
        };
      } finally {
        this.loading = false;
      }
    },
    
    async checkExportStatus() {
      if (!this.currentTaskId) return
      
      try {
        const result = await ExportService.checkStatus(this.currentTaskId)
        
        if (result.success) {
          // Check if the state has changed from in-progress to completed
          const previousState = this.exportStatus?.state
          this.exportStatus = result.data
          
          // Notify when export completes
          if (previousState && 
              (previousState === 'pending' || previousState === 'in_progress') && 
              result.data.state === 'completed') {
            // Emit success event for notification
            this.$emit('success', 'Export completed successfully! Your file is ready to download.')
            
            // Also send a notification via the notification service
            try {
              notificationService.showExport(
                'Export Complete',
                'Your quiz data export is ready to download.',
                '#exports'
              );
            } catch (err) {
              console.error('Failed to send notification:', err);
              // Continue execution even if notification fails
            }
          }
          
          // Stop checking if export is complete or failed
          if (['completed', 'failed'].includes(result.data.state)) {
            this.stopStatusChecks()
          }
        } else {
          console.error('Failed to check status:', result.message)
          this.stopStatusChecks()
        }
        
      } catch (error) {
        console.error('Failed to check export status:', error)
        this.stopStatusChecks()
      }
    },
    
    stopStatusChecks() {
      if (this.statusCheckInterval) {
        clearInterval(this.statusCheckInterval)
        this.statusCheckInterval = null
      }
    },
    
    async downloadExport() {
      if (!this.currentFilename) return
      
      this.downloading = true
      
      try {
        const result = await ExportService.downloadExport(this.currentFilename)
        
        if (!result.success) {
          this.$emit('error', result.message)
        }
        
      } catch (error) {
        console.error('Failed to download export:', error)
        this.$emit('error', 'Failed to download export. Please try again.')
      } finally {
        this.downloading = false
      }
    },
    
    getStatusClass() {
      const state = this.exportStatus?.state
      switch (state) {
        case 'completed':
          return 'alert-success'
        case 'failed':
          return 'alert-danger'
        default:
          return 'alert-info'
      }
    },
    
    getStatusIcon() {
      const state = this.exportStatus?.state
      switch (state) {
        case 'completed':
          return 'bi-check-circle'
        case 'failed':
          return 'bi-exclamation-circle'
        default:
          return 'bi-arrow-repeat spin'
      }
    },
    
    getStatusTitle() {
      const state = this.exportStatus?.state
      switch (state) {
        case 'completed':
          return 'Export Complete'
        case 'failed':
          return 'Export Failed'
        case 'pending':
          return 'Export Pending'
        default:
          return 'Export in Progress'
      }
    },

    isAuthError() {
      return this.exportStatus?.status?.includes('Authentication') ||
             this.exportStatus?.status?.includes('token') ||
             this.exportStatus?.status?.includes('log in');
    },

    redirectToLogin() {
      // Clear current token as it might be invalid
      localStorage.removeItem('token');
      
      // Redirect to login page
      window.location.href = '/login';
    }
  },
  beforeUnmount() {
    this.stopStatusChecks()
  }
}
</script>

<style scoped>
.export-manager {
  max-width: 600px;
  margin: 0 auto;
}

.alert {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.alert-success {
  border-left: 4px solid #198754;
}

.alert-danger {
  border-left: 4px solid #dc3545;
}

.alert-info {
  border-left: 4px solid #0dcaf0;
}

.alert i {
  font-size: 1.5rem;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spin {
  animation: spin 1s linear infinite;
}

.btn-primary {
  background: linear-gradient(135deg, #24a35a 0%, #1a7742 100%);
  border: none;
  padding: 0.75rem 1.5rem;
  font-weight: 500;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #1f8d4d 0%, #156437 100%);
}

.btn-primary:disabled {
  background: linear-gradient(135deg, #1a7742 0%, #135c33 100%);
  opacity: 0.7;
}
</style> 