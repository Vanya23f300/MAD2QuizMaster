<template>
  <div class="chart-component glass">
    <div class="chart-header" v-if="title || description">
      <div>
        <h4 class="text-light mb-1">{{ title }}</h4>
        <p class="text-muted mb-0" v-if="description">{{ description }}</p>
      </div>
      <div class="chart-actions" v-if="showActions">
        <div class="btn-group">
          <button 
            v-for="period in timePeriods"
            :key="period.value"
            class="btn btn-dark-toggle btn-sm"
            :class="{ 'active': selectedPeriod === period.value }"
            @click="updatePeriod(period.value)"
          >
            {{ period.label }}
          </button>
        </div>
      </div>
    </div>

    <div class="chart-content">
      <!-- Loading State -->
      <div v-if="loading" class="chart-loading">
        <div class="spinner-border text-primary"></div>
        <p class="text-muted mt-2">Loading chart data...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="chart-error">
        <i class="bi bi-exclamation-triangle text-danger"></i>
        <p class="text-danger mt-2">{{ error }}</p>
        <button class="btn btn-dark-toggle btn-sm" @click="retryLoad">
          <i class="bi bi-arrow-clockwise me-1"></i>
          Retry
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="!chartData || chartData.length === 0" class="chart-empty">
        <i class="bi bi-bar-chart"></i>
        <p class="text-muted mt-2">No data available</p>
      </div>

      <!-- Chart Container -->
      <div v-else class="chart-container">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>

    <!-- Removed legend entirely -->
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

export default {
  name: 'ChartComponent',
  props: {
    type: {
      type: String,
      required: true,
      validator: value => ['line', 'bar', 'pie', 'doughnut'].includes(value)
    },
    title: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    data: {
      type: Object,
      required: true,
      validator: value => {
        return value.labels && value.datasets
      }
    },
    options: {
      type: Object,
      default: () => ({})
    },
    showLegend: {
      type: Boolean,
      default: false // Changed default to false
    },
    showActions: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      chart: null,
      loading: false,
      error: null,
      selectedPeriod: '7d',
      hiddenDatasets: [],
      timePeriods: [
        { label: '7D', value: '7d' },
        { label: '30D', value: '30d' },
        { label: '3M', value: '3m' },
        { label: '1Y', value: '1y' }
      ]
    }
  },
  computed: {
    chartData() {
      // Create a deep copy to break reactivity chain
      return JSON.parse(JSON.stringify(this.data))
    },
    legendItems() {
      // Return empty array to avoid legend issues
      return []
    },
    defaultOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false // We're disabling the legend completely
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: 'rgba(255, 255, 255, 0.8)',
            bodyColor: 'rgba(255, 255, 255, 0.8)',
            borderColor: 'rgba(255, 255, 255, 0.1)',
            borderWidth: 1,
            padding: 10,
            boxPadding: 5
          }
        },
        scales: this.type !== 'pie' && this.type !== 'doughnut' ? {
          x: {
            grid: {
              color: 'rgba(255, 255, 255, 0.1)',
              borderColor: 'rgba(255, 255, 255, 0.2)'
            },
            ticks: {
              color: 'rgba(255, 255, 255, 0.8)'
            }
          },
          y: {
            grid: {
              color: 'rgba(255, 255, 255, 0.1)',
              borderColor: 'rgba(255, 255, 255, 0.2)'
            },
            ticks: {
              color: 'rgba(255, 255, 255, 0.8)'
            }
          }
        } : undefined
      }
    }
  },
  methods: {
    initChart() {
      try {
        const ctx = this.$refs.chartCanvas.getContext('2d')
        
        if (this.chart) {
          this.chart.destroy()
        }

        // Create a non-reactive copy of the data and options
        const chartData = JSON.parse(JSON.stringify(this.chartData))
        const chartOptions = {
          ...JSON.parse(JSON.stringify(this.defaultOptions)),
          ...JSON.parse(JSON.stringify(this.options))
        }
        
        // Forcefully disable all event handling
        chartOptions.events = []
        
        // Ensure plugins configuration exists
        if (!chartOptions.plugins) {
          chartOptions.plugins = {}
        }
        
        // Forcefully disable the legend
        chartOptions.plugins.legend = {
          display: false
        }

        this.chart = new Chart(ctx, {
          type: this.type,
          data: chartData,
          options: chartOptions
        })
      } catch (error) {
        console.error("Chart initialization error:", error)
        this.error = "Failed to initialize chart"
      }
    },
    updateChart() {
      if (!this.chart) return
      
      try {
        // Create a non-reactive copy of the data
        const chartData = JSON.parse(JSON.stringify(this.chartData))
        this.chart.data = chartData
        this.chart.update()
      } catch (error) {
        console.error("Chart update error:", error)
        this.error = "Failed to update chart"
      }
    },
    async updatePeriod(period) {
      this.selectedPeriod = period
      this.$emit('period-change', period)
    },
    async retryLoad() {
      this.error = null
      this.loading = true
      try {
        await this.$emit('retry')
      } catch (error) {
        this.error = 'Failed to load chart data'
      } finally {
        this.loading = false
      }
    },
    // eslint-disable-next-line no-unused-vars
    toggleDataset(index) {
      // This function is now effectively disabled
      console.log('Dataset toggling is disabled')
    },
    handleResize() {
      if (this.chart) {
        this.chart.resize()
      }
    }
  },
  watch: {
    data: {
      handler() {
        this.$nextTick(() => {
          if (this.chart) {
            this.updateChart()
          } else {
            this.initChart()
          }
        })
      },
      deep: true
    },
    options: {
      handler() {
        this.$nextTick(() => {
          if (this.chart) {
            try {
              // Create a non-reactive copy of the options
              const chartOptions = {
                ...JSON.parse(JSON.stringify(this.defaultOptions)),
                ...JSON.parse(JSON.stringify(this.options))
              }
              
              // Forcefully disable events
              chartOptions.events = []
              
              // Forcefully disable the legend
              if (!chartOptions.plugins) {
                chartOptions.plugins = {}
              }
              chartOptions.plugins.legend = {
                display: false
              }
              
              this.chart.options = chartOptions
              this.chart.update()
            } catch (error) {
              console.error("Chart options update error:", error)
            }
          }
        })
      },
      deep: true
    }
  },
  mounted() {
    this.$nextTick(() => {
      try {
        this.initChart()
      } catch (error) {
        console.error("Chart mount error:", error)
        this.error = "Failed to create chart"
      }
    })
    window.addEventListener('resize', this.handleResize)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
    if (this.chart) {
      try {
        this.chart.destroy()
        this.chart = null
      } catch (error) {
        console.error("Chart destroy error:", error)
      }
    }
  }
}
</script>

<style scoped>
.chart-component {
  border-radius: 1rem;
  overflow: hidden;
  padding: 1.5rem;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.chart-content {
  position: relative;
  min-height: 300px;
}

.chart-container {
  width: 100%;
  height: 300px;
  position: relative;
}

.chart-loading,
.chart-error,
.chart-empty {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  transition: all 0.2s ease;
}

.legend-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.legend-item-hidden {
  opacity: 0.5;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.875rem;
}

.legend-value {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.875rem;
  margin-left: auto;
}

.btn-group .btn {
  padding: 0.25rem 0.75rem;
}

.btn-group .btn.active {
  background-color: #24a35a !important;
  border-color: #24a35a !important;
  color: white !important;
}
</style> 