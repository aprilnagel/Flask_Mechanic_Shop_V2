import React from "react";
import "./ConfirmDelete.css";

export default function ConfirmDeleteModal({ open, onCancel, onConfirm }) {
  if (!open) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <h3>Delete Account</h3>
        <p>This action cannot be undone. Are you absolutely sure?</p>

        <div className="modal-actions">
          <button className="cancel-btn" onClick={onCancel}>
            Cancel
          </button>

          <button className="delete-btn" onClick={onConfirm}>
            Delete Account
          </button>
        </div>
      </div>
    </div>
  );
}