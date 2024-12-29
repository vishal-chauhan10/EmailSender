import { useState } from 'react';
import { 
  Paper, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  Button,
  Box,
  Alert,
  CircularProgress
} from '@mui/material';
import { Send } from '@mui/icons-material';
import { sendEmails } from '../services/api';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';

const RecipientList = ({ recipients }) => {
  const [sending, setSending] = useState(false);
  const [result, setResult] = useState(null);

  const handleSendEmails = async () => {
    setSending(true);
    setResult(null);
    
    try {
      const response = await sendEmails();
      console.log('Send emails response:', response);
      
      if (response.success) {
        setResult({
          type: 'success',
          message: response.message
        });
        toast.success(response.message);
      } else {
        throw new Error(response.message);
      }
    } catch (error) {
      console.error('Send emails error:', error);
      setResult({
        type: 'error',
        message: error.message || 'Failed to send emails'
      });
      toast.error(error.message || 'Failed to send emails');
    } finally {
      setSending(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      {result && (
        <Alert severity={result.type} sx={{ mb: 2 }}>
          {result.message}
        </Alert>
      )}
      
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>#</TableCell>
              <TableCell>Email</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {recipients.map((email, index) => (
              <TableRow key={index}>
                <TableCell>{index + 1}</TableCell>
                <TableCell>{email}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      
      <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          color="success"
          startIcon={sending ? <CircularProgress size={20} color="inherit" /> : <Send />}
          onClick={handleSendEmails}
          disabled={sending}
        >
          {sending ? 'Sending...' : 'Send Emails'}
        </Button>
      </Box>
    </Paper>
  );
};

RecipientList.propTypes = {
  recipients: PropTypes.arrayOf(PropTypes.string).isRequired
};

export default RecipientList; 