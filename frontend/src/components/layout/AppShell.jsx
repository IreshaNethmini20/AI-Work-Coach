import React from 'react';
import { Link } from 'react-router-dom';
import Icon from '../common/Icon';
export default function AppShell({ children, onStartNewTask }) { return <div className="app-shell"><header className="app-header"><Link className="brand" to="/"><span className="brand-mark"><Icon name="sparkles" size={19} /></span><span>AI Work Coach</span></Link><div className="header-actions"><Link to="/">Home</Link>{onStartNewTask && <button onClick={onStartNewTask}>Start a new task</button>}</div></header><main className="workspace">{children}</main></div>; }
