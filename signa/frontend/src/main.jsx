import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  Accessibility,
  ArrowUpRight,
  Captions,
  Check,
  ChevronDown,
  CircleHelp,
  CloudUpload,
  FileVideo,
  Gauge,
  Headphones,
  Languages,
  Library,
  Menu,
  MessageSquareText,
  Mic2,
  MoreHorizontal,
  Pause,
  Play,
  Plus,
  Radio,
  Settings2,
  ShieldCheck,
  Sparkles,
  Subtitles,
  SunMedium,
  TimerReset,
  Upload,
  Volume2,
  X,
} from 'lucide-react';
import './styles.css';

const transcript = [
  { time: '00:00', text: 'Hello, welcome back.', sign: 'HELLO', confidence: 99 },
  { time: '00:04', text: 'Today we are going to talk about', sign: 'TODAY • TALK', confidence: 96 },
  { time: '00:09', text: 'the small changes that make', sign: 'SMALL • CHANGE', confidence: 94 },
  { time: '00:13', text: 'a big difference.', sign: 'BIG • DIFFERENCE', confidence: 98 },
  { time: '00:17', text: 'Let’s get started.', sign: 'START', confidence: 97 },
];

const languages = ['ASL', 'BSL', 'Auslan', 'ISL'];

function App() {
  const videoRef = useRef(null);
  const fileInputRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [captions, setCaptions] = useState(true);
  const [translate, setTranslate] = useState(true);
  const [activeLanguage, setActiveLanguage] = useState('ASL');
  const [languageOpen, setLanguageOpen] = useState(false);
  const [showUpload, setShowUpload] = useState(false);
  const [currentTime, setCurrentTime] = useState(7.8);
  const [duration, setDuration] = useState(60);
  const [volume, setVolume] = useState(82);
  const [activeTranscript, setActiveTranscript] = useState(1);
  const [fileName, setFileName] = useState('The small changes that make a big difference');
  const [toast, setToast] = useState('');

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    const onTime = () => {
      setCurrentTime(video.currentTime);
      if (video.duration && Number.isFinite(video.duration)) setDuration(video.duration);
      const idx = Math.min(transcript.length - 1, Math.floor(video.currentTime / 4.5));
      setActiveTranscript(idx);
    };
    const onPlay = () => setIsPlaying(true);
    const onPause = () => setIsPlaying(false);
    const onMetadata = () => {
      if (video.duration && Number.isFinite(video.duration)) setDuration(video.duration);
    };
    video.addEventListener('timeupdate', onTime);
    video.addEventListener('play', onPlay);
    video.addEventListener('pause', onPause);
    video.addEventListener('loadedmetadata', onMetadata);
    return () => {
      video.removeEventListener('timeupdate', onTime);
      video.removeEventListener('play', onPlay);
      video.removeEventListener('pause', onPause);
      video.removeEventListener('loadedmetadata', onMetadata);
    };
  }, []);

  useEffect(() => {
    if (videoRef.current) videoRef.current.volume = volume / 100;
  }, [volume]);

  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => setToast(''), 2600);
    return () => clearTimeout(timer);
  }, [toast]);

  const progress = useMemo(() => `${Math.min(100, (currentTime / duration) * 100)}%`, [currentTime, duration]);

  const togglePlay = () => {
    const video = videoRef.current;
    if (!video) return;
    if (video.paused) video.play().catch(() => setIsPlaying((v) => !v));
    else video.pause();
  };

  const seek = (event) => {
    const value = Number(event.target.value);
    setCurrentTime(value);
    if (videoRef.current) videoRef.current.currentTime = value;
  };

  const selectTranscript = (index) => {
    const nextTime = index * 4.5;
    setActiveTranscript(index);
    setCurrentTime(nextTime);
    if (videoRef.current) videoRef.current.currentTime = nextTime;
  };

  const chooseFile = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setFileName(file.name.replace(/\.[^/.]+$/, ''));
    if (videoRef.current) videoRef.current.src = URL.createObjectURL(file);
    setShowUpload(false);
    setToast('Video added · live translation is ready');
  };

  const showToast = (message) => setToast(message);

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand-lockup">
          <div className="brand-mark" aria-hidden="true"><span></span><span></span><span></span></div>
          <span className="brand-name">signa</span>
          <span className="beta-pill">BETA</span>
        </div>
        <nav className="main-nav" aria-label="Main navigation">
          <button className="nav-link active"><Radio size={15} /> Live player</button>
          <button className="nav-link" onClick={() => showToast('Your saved videos will appear here soon')}><Library size={15} /> My library</button>
        </nav>
        <div className="top-actions">
          <button className="icon-button subtle" aria-label="Help" onClick={() => showToast('Need help? Try uploading any MP4 or MOV video')}><CircleHelp size={18} /></button>
          <div className="profile-chip"><span className="avatar">JD</span><span className="profile-name">Jordan</span><ChevronDown size={14} /></div>
        </div>
      </header>

      <main className="page-content">
        <div className="page-heading">
          <div>
            <p className="eyebrow"><span className="live-dot"></span> LIVE TRANSLATION</p>
            <h1>Watch anything.<br /><em>Understand everything.</em></h1>
          </div>
          <button className="upload-cta" onClick={() => setShowUpload(true)}><Plus size={17} /> Add a video <ArrowUpRight size={15} /></button>
        </div>

        <section className="workspace" aria-label="Video translation workspace">
          <div className="player-column">
            <div className="video-frame">
              <video
                ref={videoRef}
                className="video-element"
                poster="https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=1600&q=85"
                src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
                playsInline
                aria-label="A video ready for live sign language translation"
              />
              <div className="video-shade"></div>
              <div className="video-topline">
                <div className="video-source"><span className="source-icon"><FileVideo size={14} /></span><span>{fileName}</span></div>
                <button className="video-more" aria-label="More video options"><MoreHorizontal size={21} /></button>
              </div>
              {captions && <div className="video-caption"><span>Today we are going to talk about</span><small>English · Auto-generated</small></div>}
              <div className="video-center-control"><button className="big-play" onClick={togglePlay} aria-label={isPlaying ? 'Pause video' : 'Play video'}>{isPlaying ? <Pause fill="currentColor" size={26} /> : <Play fill="currentColor" size={26} />}</button></div>
              <div className="video-controls">
                <div className="timeline-wrap"><input aria-label="Video progress" type="range" min="0" max={duration} step="0.1" value={Math.min(currentTime, duration)} onChange={seek} style={{ '--progress': progress }} /></div>
                <div className="control-row">
                  <div className="control-group">
                    <button className="control-button" onClick={togglePlay} aria-label={isPlaying ? 'Pause' : 'Play'}>{isPlaying ? <Pause fill="currentColor" size={17} /> : <Play fill="currentColor" size={17} />}</button>
                    <button className="control-button" onClick={() => setVolume((v) => v ? 0 : 82)} aria-label="Toggle sound"><Volume2 size={17} /></button>
                    <span className="time-readout">{formatTime(currentTime)} <i>/</i> {formatTime(duration)}</span>
                  </div>
                  <div className="control-group">
                    <button className={`control-button ${captions ? 'selected' : ''}`} onClick={() => setCaptions((v) => !v)} aria-label="Toggle captions"><Captions size={17} /></button>
                    <button className="speed-button" onClick={() => showToast('Playback speed set to 1×')}>1×</button>
                    <button className="control-button" aria-label="Video settings" onClick={() => showToast('Video settings are ready')}><Settings2 size={17} /></button>
                  </div>
                </div>
              </div>
            </div>
            <div className="video-meta">
              <div><h2>{fileName}</h2><p>With Signa · 1 min watch · Added today</p></div>
              <div className="meta-actions"><button className="outline-button" onClick={() => showToast('Share link copied to clipboard')}><ArrowUpRight size={15} /> Share</button><button className="round-button" aria-label="More options"><MoreHorizontal size={19} /></button></div>
            </div>

            <div className="transcript-panel">
              <div className="panel-heading"><div><p className="eyebrow">TRANSLATION TIMELINE</p><h3>Follow along</h3></div><button className="transcript-options" onClick={() => showToast('Transcript exported as a text file')}><Upload size={14} /> Export transcript</button></div>
              <div className="transcript-list">
                {transcript.map((item, index) => <button key={item.time} className={`transcript-row ${activeTranscript === index ? 'current' : ''}`} onClick={() => selectTranscript(index)}><span className="transcript-time">{item.time}</span><span className="transcript-copy"><strong>{item.text}</strong><small>{item.sign}</small></span><span className="confidence"><span className="confidence-bar"><i style={{ width: `${item.confidence}%` }}></i></span>{item.confidence}%</span>{activeTranscript === index && <Check className="transcript-check" size={15} />}</button>)}
              </div>
            </div>
          </div>

          <aside className="translation-panel">
            <div className="translation-header"><div className="translation-title"><div className="translation-icon"><Accessibility size={20} /></div><div><p className="eyebrow">SIGN LANGUAGE</p><h2>Live translation</h2></div></div><span className="status-pill"><span></span> Active</span></div>
            <div className={`translator-card ${!translate ? 'translation-paused' : ''}`}>
              <div className="translator-stage">
                <div className="stage-badge"><Sparkles size={12} /> {translate ? 'Translating now' : 'Translation paused'}</div>
                <div className="person-illustration" aria-label="Animated sign language interpreter placeholder">
                  <div className="halo"></div><div className="person-head"></div><div className="person-neck"></div><div className="person-body"></div><div className="person-arm left"></div><div className="person-arm right"></div><div className="person-hand left"></div><div className="person-hand right"></div>
                </div>
                <div className="sign-label"><span className="mini-live"></span><b>{translate ? transcript[activeTranscript].sign : 'PAUSED'}</b><small>{translate ? 'American Sign Language' : 'Translation layer is off'}</small></div>
              </div>
              <div className="translator-status"><div><span className="status-check"><Check size={12} /></span><span>High confidence</span></div><strong>{transcript[activeTranscript].confidence}%</strong></div>
            </div>
            <div className="translation-settings">
              <div className="setting-row"><div className="setting-label"><Languages size={17} /><span>Language</span></div><div className="select-wrap"><button className="language-select" onClick={() => setLanguageOpen((v) => !v)}>{activeLanguage}<ChevronDown size={14} /></button>{languageOpen && <div className="language-menu">{languages.map((language) => <button key={language} onClick={() => { setActiveLanguage(language); setLanguageOpen(false); showToast(`${language} translation selected`); }}>{language}{activeLanguage === language && <Check size={14} />}</button>)}</div>}</div></div>
              <div className="setting-row"><div className="setting-label"><Subtitles size={17} /><span>Captions</span></div><button className={`toggle ${captions ? 'on' : ''}`} onClick={() => setCaptions((v) => !v)} aria-label="Toggle captions"><span></span></button></div>
              <div className="setting-row"><div className="setting-label"><MessageSquareText size={17} /><span>Translation</span></div><button className={`toggle ${translate ? 'on' : ''}`} onClick={() => setTranslate((v) => !v)} aria-label="Toggle sign translation"><span></span></button></div>
            </div>
            <div className="panel-note"><ShieldCheck size={15} /><span>Your video stays private. Signa processes it securely in your browser.</span></div>
          </aside>
        </section>

        <section className="how-it-works"><div className="how-title"><p className="eyebrow">MADE FOR REAL LIFE</p><h2>Make every video<br /><em>more welcoming.</em></h2></div><div className="how-steps"><div className="how-step"><span>01</span><div className="step-icon"><CloudUpload size={19} /></div><h3>Add your video</h3><p>Upload a file or paste a link from your favorite platform.</p></div><div className="how-step"><span>02</span><div className="step-icon"><Radio size={19} /></div><h3>Turn on Signa</h3><p>Get a live sign language layer that follows the action.</p></div><div className="how-step"><span>03</span><div className="step-icon"><Headphones size={19} /></div><h3>Watch your way</h3><p>Adjust captions, language, and speed whenever you need.</p></div></div></section>
      </main>

      <footer className="footer"><div className="footer-brand"><div className="brand-mark small"><span></span><span></span><span></span></div><span>signa</span></div><span>Built for a more accessible internet.</span><div className="footer-links"><button onClick={() => showToast('Accessibility settings are coming soon')}>Accessibility</button><button onClick={() => showToast('Privacy-first by design')}>Privacy</button><button onClick={() => showToast('Thanks for helping shape Signa')}>Feedback <ArrowUpRight size={13} /></button></div></footer>

      {showUpload && <div className="modal-backdrop" onClick={() => setShowUpload(false)}><div className="upload-modal" onClick={(event) => event.stopPropagation()}><button className="modal-close" onClick={() => setShowUpload(false)} aria-label="Close"><X size={18} /></button><div className="modal-icon"><CloudUpload size={24} /></div><p className="eyebrow">ADD TO YOUR LIBRARY</p><h2>Bring your own video.</h2><p className="modal-copy">Signa can translate videos as you watch them. Start with an MP4, MOV, or WebM file.</p><button className="drop-zone" onClick={() => fileInputRef.current?.click()}><Upload size={21} /><strong>Choose a video file</strong><span>or drag and drop it here</span></button><input ref={fileInputRef} type="file" accept="video/mp4,video/quicktime,video/webm" hidden onChange={chooseFile} /><p className="modal-footnote"><ShieldCheck size={14} /> Your file stays on your device in this demo.</p></div></div>}
      {toast && <div className="toast"><Check size={15} /> {toast}</div>}
    </div>
  );
}

function formatTime(seconds) {
  const safe = Math.max(0, Math.floor(seconds));
  return `${String(Math.floor(safe / 60)).padStart(2, '0')}:${String(safe % 60).padStart(2, '0')}`;
}

createRoot(document.getElementById('root')).render(<App />);
