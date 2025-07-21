/**
 * Utility functions for handling Bootstrap modals
 */

export const cleanupModals = () => {
  // Remove all modal backdrops
  document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
    backdrop.remove();
  });

  // Remove modal-open class and inline styles from body
  document.body.classList.remove('modal-open');
  document.body.style.removeProperty('overflow');
  document.body.style.removeProperty('padding-right');

  // Hide any open modals
  document.querySelectorAll('.modal').forEach(modalEl => {
    modalEl.classList.remove('show');
    modalEl.style.display = 'none';
    modalEl.setAttribute('aria-hidden', 'true');
  });
};

export const showModal = (modalId) => {
  // First cleanup any existing modals
  cleanupModals();

  // Get the modal element
  const modalEl = document.getElementById(modalId);
  if (!modalEl) return;

  // Show the modal
  modalEl.style.display = 'block';
  modalEl.classList.add('show');
  modalEl.removeAttribute('aria-hidden');
  
  // Add modal-open class to body
  document.body.classList.add('modal-open');
};

export const hideModal = (modalId) => {
  const modalEl = document.getElementById(modalId);
  if (!modalEl) return;

  // Hide the modal
  modalEl.classList.remove('show');
  modalEl.style.display = 'none';
  modalEl.setAttribute('aria-hidden', 'true');

  // Cleanup
  cleanupModals();
}; 