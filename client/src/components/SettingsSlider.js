import React from 'react';
import Slider from '@mui/material/Slider';
import {Typography} from "@mui/material";

export default function  SettingsSlider ( { value, onChange, min, max, step, label }) {
    return (
        <div>
            <Slider
                value={value}
                onChange={onChange}
                aria-labelledby="discrete-slider"
                valueLabelDisplay="auto"
                step={step}
                min={min}
                max={max}
            />
            <Typography variant="caption" align="center">
                {label}
            </Typography>
        </div>
    );
};


