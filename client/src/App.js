import React, { useState } from 'react';
import axios from 'axios';
import { Box, CircularProgress, Grid } from '@mui/material';
import { PromptField, SettingsSlider, SubmitButton } from './components';

const App = () => {
    const [prompt, setPrompt] = useState('');
    const [numInference, setNumInference] = useState(50);
    const [guidanceScale, setGuidanceScale] = useState(7.5);
    const [negativePrompt, setNegativePrompt] = useState('');
    const [loading, setLoading] = useState(false);
    const [imageSrc, setImageSrc] = useState('');

    const handlePromptChange = (e) => {
        setPrompt(e.target.value);
    };

    const handleNegativePromptChange = (e) => {
        setNegativePrompt(e.target.value);
    };

    const handleInferenceChange = (e, newValue) => {
        setNumInference(newValue);
    };

    const handleGuidanceScale = (e, newValue) => {
        setGuidanceScale(newValue);
    };

    const handleSubmit = async () => {
        setLoading(true);
        try {
            const response = await axios.post(process.env.REACT_APP_ENDPOINT_URL, {
                prompt: prompt,
                num_inference: numInference,
                guidance_scale: guidanceScale,
                negative_prompt: negativePrompt,
                height: 512,
                width: 512,
                num_images: 1,
            }, {
                responseType: "arraybuffer"
            });

            const blob = new Blob([response.data], { type: 'image/png' });
            const objectUrl = URL.createObjectURL(blob);

            setImageSrc(objectUrl);
        } catch (error) {
            console.error(error);
        }
        setLoading(false);
    };


    return (
        <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
            <Box sx={{ width: 300, height: 300, border: '1px solid gray', marginBottom: 4, position: 'relative' }}>
                {loading && <CircularProgress sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }} />}
                {imageSrc && <img src={imageSrc} alt="AI-generated image" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />}
            </Box>
            <Grid container spacing={1} justifyContent="center" alignItems="center">
                <Grid item container xs={6} justifyContent="center">
                    <PromptField value={prompt} onChange={handlePromptChange} label="Prompt" />
                </Grid>
                <Grid item xs={6}>
                    <PromptField value={negativePrompt} onChange={handleNegativePromptChange} label="Negative Prompt" />
                </Grid>
                <Grid item xs={2} sx={{ padding: '0 8px' }}>
                    <SettingsSlider value={numInference} onChange={handleInferenceChange} step={1} min={1} max={50} label="Num Inferences Steps" />
                </Grid>
                <Grid item xs={2} sx={{ padding: '0 8px' }}>
                    <SettingsSlider value={guidanceScale} onChange={handleGuidanceScale} step={0.5} min={0.0} max={12.0} label="Guidance Scale" />
                </Grid>
                <Grid item xs={12} container justifyContent="center">
                    <SubmitButton onClick={handleSubmit} />
                </Grid>
            </Grid>
        </Box>
    );
};

export default App;
