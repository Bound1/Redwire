import React from 'react';
import TextField from '@mui/material/TextField';

export default function PromptField ( {value, onChange,label} ){
    return (
        <TextField
            label={label}
            value={value}
            onChange={onChange}
            variant="outlined"
        />
    );
};

