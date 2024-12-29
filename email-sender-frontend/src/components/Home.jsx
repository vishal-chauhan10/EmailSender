import { useState } from 'react';
import { 
  Container, 
  Paper, 
  Button, 
  Typography,
  Box,
  CircularProgress 
} from '@mui/material';
import { Upload } from '@mui/icons-material';
import { uploadCSV } from '../services/api';
import { toast } from 'react-toastify';
import RecipientList from './RecipientList';

const Home = () => {
  const [file, setFile] = useState(null);
  const [recipients, setRecipients] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      toast.error('Please select a file');
      return;
    }

    setLoading(true);
    try {
      const response = await uploadCSV(file);
      setRecipients(response.recipients || []);
      toast.success('File uploaded successfully!');
    } catch (error) {
      toast.error(error.message || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4 }}>
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            Upload CSV File
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            <Button
              variant="contained"
              component="label"
              startIcon={<Upload />}
              disabled={loading}
            >
              Select File
              <input
                type="file"
                hidden
                accept=".csv"
                onChange={handleFileChange}
              />
            </Button>
            {file && (
              <>
                <Typography>{file.name}</Typography>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleUpload}
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : 'Upload'}
                </Button>
              </>
            )}
          </Box>
        </Paper>

        {recipients.length > 0 && (
          <RecipientList recipients={recipients} />
        )}
      </Box>
    </Container>
  );
};

export default Home; 