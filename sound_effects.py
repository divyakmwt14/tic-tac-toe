"""
Procedural Audio Generator for Quantum Tic-Tac-Toe
Generates high quality 16-bit PCM sound effects using NumPy and Pygame mixer.
Requires no external .wav or .mp3 files!
"""

import numpy as np
import pygame

class SoundManager:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.muted = False
        self.sounds = {}
        self.initialized = False
        self._init_mixer()

    def _init_mixer(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=2, buffer=512)
            self.initialized = True
            self._generate_all_sounds()
        except Exception as e:
            print(f"[SoundManager] Warning: Audio init failed ({e}). Running in silent mode.")
            self.initialized = False

    def toggle_mute(self):
        self.muted = not self.muted
        return self.muted

    def _to_stereo_sound(self, mono_samples):
        # Normalize and convert to 16-bit signed integers
        mono_samples = np.clip(mono_samples, -1.0, 1.0)
        int16_samples = (mono_samples * 32767).astype(np.int16)
        stereo_samples = np.column_stack((int16_samples, int16_samples))
        return pygame.sndarray.make_sound(stereo_samples)

    def _generate_all_sounds(self):
        if not self.initialized:
            return

        # 1. Move Placement: Quantum bell chime (587 Hz D5 -> 880 Hz A5 dual tone with bell decay)
        t_move = np.linspace(0, 0.22, int(self.sample_rate * 0.22), endpoint=False)
        env_move = np.exp(-12 * t_move)
        wave_move = 0.5 * np.sin(2 * np.pi * 659.25 * t_move) + 0.35 * np.sin(2 * np.pi * 987.77 * t_move)
        self.sounds['move'] = self._to_stereo_sound(wave_move * env_move)

        # 2. Entanglement / Cycle Formed: Ominous pulsing resonant wave
        t_loop = np.linspace(0, 0.45, int(self.sample_rate * 0.45), endpoint=False)
        env_loop = np.sin(np.pi * t_loop / 0.45) ** 0.6
        # Beating frequencies (260 Hz & 266 Hz) for an eerie quantum superposition resonance
        wave_loop = 0.5 * np.sin(2 * np.pi * 261.63 * t_loop) + 0.5 * np.sin(2 * np.pi * 267.63 * t_loop)
        # Add harmonic
        wave_loop += 0.25 * np.sin(2 * np.pi * 523.25 * t_loop)
        self.sounds['loop'] = self._to_stereo_sound(wave_loop * env_loop)

        # 3. Collapse: Quantum discharge / descending energy sweep
        t_col = np.linspace(0, 0.5, int(self.sample_rate * 0.5), endpoint=False)
        freq_sweep = 900.0 * np.exp(-6.0 * t_col) + 120.0
        phase = 2 * np.pi * np.cumsum(freq_sweep) / self.sample_rate
        env_col = np.exp(-5.5 * t_col)
        # Add noise sparkle
        noise = (np.random.rand(len(t_col)) * 2 - 1) * np.exp(-15 * t_col) * 0.3
        wave_col = 0.7 * np.sin(phase) + noise
        self.sounds['collapse'] = self._to_stereo_sound(wave_col * env_col)

        # 4. Victory / Triumph: Sci-fi arpeggiated major chord
        duration = 0.7
        t_win = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        env_win = np.exp(-3.5 * t_win)
        notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
        wave_win = np.zeros_like(t_win)
        seg_len = len(t_win) // 4
        for i, f in enumerate(notes):
            start = i * (seg_len // 2)
            end = len(t_win)
            t_sub = t_win[start:end] - t_win[start]
            env_sub = np.exp(-4.0 * t_sub)
            wave_win[start:end] += 0.3 * np.sin(2 * np.pi * f * t_sub) * env_sub
        self.sounds['win'] = self._to_stereo_sound(wave_win)

        # 5. UI Click: Snappy high-frequency tick
        t_click = np.linspace(0, 0.05, int(self.sample_rate * 0.05), endpoint=False)
        env_click = np.exp(-50 * t_click)
        wave_click = np.sin(2 * np.pi * 1200 * t_click) * env_click
        self.sounds['click'] = self._to_stereo_sound(wave_click)

    def play(self, sound_name):
        if self.muted or not self.initialized:
            return
        snd = self.sounds.get(sound_name)
        if snd:
            snd.play()
