# Windows-Shutdown-Scheduler

[![Downloads](https://img.shields.io/github/downloads/ElAlehYT/Windows-Shutdown-Scheduler/total?color=blue&label=Downloads)](https://github.com/ElAlehYT/Windows-Shutdown-Scheduler/releases)
[![Latest Release](https://img.shields.io/github/v/release/ElAlehYT/Windows-Shutdown-Scheduler?label=latest%20release&color=success)](https://github.com/ElAlehYT/Windows-Shutdown-Scheduler/releases/latest)
[![Stars](https://img.shields.io/github/stars/ElAlehYT/Windows-Shutdown-Scheduler?style=social)](https://github.com/ElAlehYT/Windows-Shutdown-Scheduler/stargazers)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-informational)
![License](https://img.shields.io/badge/License-MIT-green)

Windows-Shutdown-Scheduler is a lightweight desktop app to **schedule your PC's shutdown** quickly and visually. Features an animated countdown ring, system tray support, fullscreen game detection, automatic shutdown when a download finishes, and native Windows notifications. Available in **Spanish and English**, auto-detected from your Windows language.

> ⚠️ **Windows Defender may show a popup** saying "Windows protected your PC" when opening the `.exe`, since it isn't digitally signed. Just click **More info** → **Run anyway**. This is normal for open-source apps without a signing certificate.

## ✨ Features

- **Quick presets**: Now, 1, 5, 15, 30 min, or 1 hour — one click away.
- **Custom time**: set an exact number of hours, minutes, and seconds.
- **Animated countdown**: real-time circular progress ring.
- **System tray support**: minimize the app and it keeps running in the background.
- **Fullscreen game detection**: warns you and lets you postpone the shutdown by 10 minutes if a fullscreen app/game is active, so it won't interrupt your session.
- **Shut down when a download finishes**: monitors your network speed and automatically shuts down once an active download (Steam, Epic Games, Battle.net, etc.) stops.
- **Native Windows toast notifications**: on scheduling, cancelling, and when 1 minute is left.
- **Persistent settings**: remembers the last custom time you used.
- **Keyboard shortcut**: `Esc` instantly cancels a running shutdown or download monitor.
- **Bilingual interface**: automatically detects and switches between Spanish and English based on your Windows language, with a manual ES/EN toggle.

## 📥 Download

Grab the latest version directly from [**Releases**](https://github.com/ElAlehYT/Windows-Shutdown-Scheduler/releases/latest). Just download the `.exe` and run it — everything needed is already bundled in, no installation required.

### Something not working?

If a feature doesn't work (tray icon, notifications, or the download-monitor option), it's likely running from source without the optional libraries. Install them with:

```bash
pip install pystray pillow win10toast psutil
```

- `pystray` + `pillow` → system tray icon
- `win10toast` → native toast notifications
- `psutil` → network monitoring for the "shut down when a download finishes" feature

The app runs fine without them too — those specific features just won't be available.

## 📸 Screenshots

*(add a GIF or screenshot of the app in action here)*

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

## 👤 Author

**ElAlehYT**

- YouTube: https://www.youtube.com/@elalehyt
- TikTok: https://www.tiktok.com/@elalehyt
- Twitch: https://www.twitch.tv/elalehyt
- All my links: https://linktr.ee/ElAlehYT
- Website: https://website.beacons.ai/elaleh

---

## 🇪🇸 Español

Windows-Shutdown-Scheduler es una app de escritorio ligera para **programar el apagado de tu PC** de forma rápida y visual. Incluye un countdown animado, bandeja del sistema, detección de juegos a pantalla completa, apagado automático cuando termina una descarga, y notificaciones nativas de Windows. Disponible en **español e inglés**, detectado automáticamente según el idioma de tu Windows.

> ⚠️ **Windows Defender puede mostrar un aviso** diciendo "Windows protegió tu PC" al abrir el `.exe`, ya que no está firmado digitalmente. Haz clic en **Más información** → **Ejecutar de todas formas**. Esto es normal en apps de código abierto sin certificado de firma.

### ✨ Características

- **Temporizadores rápidos**: Ahora, 1, 5, 15, 30 min o 1 hora, con un solo clic.
- **Tiempo personalizado**: define horas, minutos y segundos exactos.
- **Countdown animado**: anillo de progreso circular en tiempo real.
- **Bandeja del sistema**: minimiza la app y sigue funcionando en segundo plano.
- **Detección de juego a pantalla completa**: avisa y permite posponer el apagado 10 minutos si detecta una app fullscreen activa, para no cortar tu partida.
- **Apagar cuando termine una descarga**: mide la velocidad de tu red y apaga el PC automáticamente cuando una descarga activa (Steam, Epic Games, Battle.net, etc.) se detiene.
- **Notificaciones nativas de Windows**: al programar, cancelar, o cuando queda 1 minuto.
- **Configuración persistente**: recuerda el último tiempo personalizado usado.
- **Atajo de teclado**: `Esc` cancela al instante un apagado o el monitor de descargas en curso.
- **Interfaz bilingüe**: detecta y cambia automáticamente entre español e inglés según el idioma de tu Windows, con un botón manual ES/EN.

### 📥 Descarga

Descarga la última versión desde [**Releases**](https://github.com/ElAlehYT/Windows-Shutdown-Scheduler/releases/latest). Solo baja el `.exe` y ejecútalo — todo lo necesario ya viene incluido, no requiere instalación.

### ¿Algo no funciona?

Si alguna función no funciona (icono de bandeja, notificaciones, o la opción de apagado por descarga), probablemente estás ejecutando el código fuente sin las librerías opcionales. Instálalas con:

```bash
pip install pystray pillow win10toast psutil
```

- `pystray` + `pillow` → icono de la bandeja del sistema
- `win10toast` → notificaciones nativas
- `psutil` → monitoreo de red para la función de "apagar cuando termine una descarga"

La app funciona igual sin ellas, simplemente esas funciones concretas no estarán disponibles.

### 📄 Licencia

Este proyecto está bajo la licencia MIT — consulta [LICENSE](LICENSE) para más detalles.

### 👤 Autor

**ElAlehYT**

- YouTube: https://www.youtube.com/@elalehyt
- TikTok: https://www.tiktok.com/@elalehyt
- Twitch: https://www.twitch.tv/elalehyt
- Todos mis enlaces: https://linktr.ee/ElAlehYT
- Web: https://website.beacons.ai/elaleh
