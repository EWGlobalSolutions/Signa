# Signa — live video translation

Signa is a polished, accessibility-first front-end for watching videos with a real-time sign-language translation layer. It includes a working video player, local video upload, transcript seeking, language selection, caption and translation toggles, and responsive layouts for desktop and mobile.

## Run locally

```bash
npm install
npm run dev
```

Then open the local Vite URL shown in the terminal.

## Build for distribution

```bash
npm run build
npm run preview
```

The production output is written to `dist/` and can be served by any static host.

## Product boundary

The interface is wired for a real translation service, but the interpreter panel currently uses a visual demo state and a sample transcript. To make it production-real, connect the active video time to a streaming inference service and replace the sample `transcript` data in `src/main.jsx` with timestamped translation events. The local upload flow is already wired to the native `<video>` element, so files selected by the viewer play immediately in the player.

## Included interactions

- Native video playback, seeking, duration, and volume state
- Local MP4, MOV, and WebM upload
- Transcript rows that seek the video
- ASL / BSL / Auslan / ISL language selector
- Captions and sign-translation toggles
- Export, share, help, privacy, and feedback affordances with feedback toasts
- Responsive layout for smaller screens
