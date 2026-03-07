/**
 * API Configuration Helper
 * 
 * This file provides the environment variable method for the API base URL.
 * 
 * Usage (once you are ready to update Services.jsx):
 * import { API_BASE_URL } from '../config';
 * 
 * Then replace:
 * fetch("http://localhost:8000/analyze"...)
 * With:
 * fetch(`${API_BASE_URL}/analyze`...)
 */

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
