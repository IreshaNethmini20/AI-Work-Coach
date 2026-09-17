import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import CoachPage from './pages/CoachPage';
import LandingPage from './pages/LandingPage';
import './styles/variables.css';
import './index.css';
export default function App() { return <BrowserRouter><Routes><Route path="/" element={<LandingPage />} /><Route path="/coach" element={<CoachPage />} /></Routes></BrowserRouter>; }
