import React from 'react';
import Button from '@mui/material/Button';

export default function SubmitButton ( {onClick} ){
    return (
        <Button variant="contained" color="primary" onClick={onClick}>
            Generate Image
        </Button>
    );
};


