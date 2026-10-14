"""
Catppuccin Theme and Neon Glow Rendering System for Quantum Tic-Tac-Toe
Provides glowing geometry, floating quantum particle simulation, and sci-fi aesthetic.
"""

import math
import random
import pygame

# --- Catppuccin Mocha Palette ---
COLOR_CRUST = (17, 17, 27)
COLOR_MANTLE = (24, 24, 37)
COLOR_BASE = (30, 30, 46)
COLOR_SURFACE0 = (49, 50, 68)
COLOR_SURFACE1 = (69, 71, 90)
COLOR_SURFACE2 = (88, 91, 112)
COLOR_OVERLAY = (108, 112, 134)
COLOR_TEXT = (205, 214, 244)
COLOR_SUBTEXT = (166, 173, 200)

# Neon Accents
COLOR_CYAN = (137, 220, 235)      # Player X
COLOR_MAUVE = (203, 166, 247)     # Player O
COLOR_RED = (243, 139, 168)       # Cycle / Alert
COLOR_GREEN = (166, 227, 161)     # Win / Classical
COLOR_YELLOW = (249, 226, 175)    # Highlights
COLOR_LAVENDER = (180, 190, 254)  # Entanglement Links

class Particle:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.x = random.uniform(0, w)
        self.y = random.uniform(0, h)
        self.vx = random.uniform(-0.35, 0.35)
        self.vy = random.uniform(-0.35, 0.35)
        self.radius = random.uniform(1.2, 2.8)
        self.alpha = random.randint(40, 140)
        self.phase = random.uniform(0, math.pi * 2)
        self.color = random.choice([COLOR_CYAN, COLOR_MAUVE, COLOR_LAVENDER])

    def update(self):
        self.x = (self.x + self.vx) % self.w
        self.y = (self.y + self.vy) % self.h
        self.phase += 0.03

    def draw(self, surface):
        pulsing_alpha = int(self.alpha * (0.6 + 0.4 * math.sin(self.phase)))
        p_surf = pygame.Surface((int(self.radius * 4), int(self.radius * 4)), pygame.SRCALPHA)
        color_with_alpha = (*self.color, pulsing_alpha)
        pygame.draw.circle(p_surf, color_with_alpha, (int(self.radius * 2), int(self.radius * 2)), int(self.radius))
        surface.blit(p_surf, (int(self.x - self.radius * 2), int(self.y - self.radius * 2)))


class Starfield:
    def __init__(self, w, h, count=55):
        self.particles = [Particle(w, h) for _ in range(count)]

    def update_and_draw(self, surface):
        for p in self.particles:
            p.update()
            p.draw(surface)


def draw_neon_line(surface, color, start_pos, end_pos, width=3, glow_layers=3):
    """Draws a line with glowing multi-layer alpha halo."""
    glow_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    for layer in range(glow_layers, 0, -1):
        alpha = int(35 / layer)
        lw = width + layer * 3
        pygame.draw.line(glow_surface, (*color, alpha), start_pos, end_pos, lw)
    pygame.draw.line(surface, color, start_pos, end_pos, width)
    surface.blit(glow_surface, (0, 0))


def draw_neon_rect(surface, color, rect, border_radius=12, width=2, glow_layers=3):
    """Draws a rounded rect with soft glowing border."""
    glow_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    for layer in range(glow_layers, 0, -1):
        alpha = int(30 / layer)
        lw = width + layer * 2
        pygame.draw.rect(glow_surface, (*color, alpha), rect, lw, border_radius=border_radius)
    pygame.draw.rect(surface, color, rect, width, border_radius=border_radius)
    surface.blit(glow_surface, (0, 0))


def draw_neon_circle(surface, color, center, radius, width=2, glow_layers=3):
    """Draws a circle with glowing outline."""
    glow_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    for layer in range(glow_layers, 0, -1):
        alpha = int(35 / layer)
        r = radius + layer * 2
        pygame.draw.circle(glow_surface, (*color, alpha), center, r, width + layer)
    pygame.draw.circle(surface, color, center, radius, width)
    surface.blit(glow_surface, (0, 0))


def draw_glowing_text(surface, text, font, color, center, glow_radius=4):
    """Renders text with an ambient neon back-glow."""
    glow_surf = font.render(text, True, color)
    w, h = glow_surf.get_size()
    # Draw soft shadow offsets
    alpha_surf = pygame.Surface((w + glow_radius * 2, h + glow_radius * 2), pygame.SRCALPHA)
    for dx in range(-glow_radius, glow_radius + 1, 2):
        for dy in range(-glow_radius, glow_radius + 1, 2):
            if dx == 0 and dy == 0:
                continue
            t = font.render(text, True, (*color, 25))
            alpha_surf.blit(t, (dx + glow_radius, dy + glow_radius))
    
    # Blit halo
    surface.blit(alpha_surf, (center[0] - w // 2 - glow_radius, center[1] - h // 2 - glow_radius))
    # Blit crisp foreground text
    fg_surf = font.render(text, True, color)
    surface.blit(fg_surf, (center[0] - w // 2, center[1] - h // 2))
