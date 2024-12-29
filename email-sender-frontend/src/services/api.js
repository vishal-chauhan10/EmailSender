import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5001',
  withCredentials: true,  // Important for sessions
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

export const login = async (username, password) => {
  console.log('Starting login attempt...');
  try {
    // Try direct fetch to test API connectivity
    const response = await fetch('http://localhost:5001/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
      credentials: 'include'
    });

    console.log('Raw response:', response);
    const data = await response.json();
    console.log('Response data:', data);

    if (data.success) {
      return data;
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    console.error('Detailed login error:', {
      error,
      message: error.message,
      stack: error.stack
    });
    throw new Error('Login failed - please check if the server is running');
  }
};

export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await api.post('/home', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw error.response?.data?.message || 'Upload failed';
  }
};

export const sendEmails = async () => {
  try {
    console.log('Sending emails...');
    const response = await api.post('/send-emails');
    console.log('Send emails response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Send emails error:', error);
    throw new Error(error.response?.data?.message || 'Failed to send emails');
  }
};

export const logout = async () => {
  try {
    await api.get('/logout');
  } catch (error) {
    console.error('Logout failed:', error);
  }
}; 