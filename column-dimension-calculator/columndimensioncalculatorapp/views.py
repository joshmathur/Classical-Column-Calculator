from django.shortcuts import render
import math
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime

# ── Enums / Dataclasses ──────────────────────────────────────────

class Material(Enum):
    MARBLE    = (2550, "Pentelic Marble")
    LIMESTONE = (2300, "Limestone")
    GRANITE   = (2700, "Granite")

    def __init__(self, density: float, description: str):
        self.density = density
        self.description = description


@dataclass
class ColumnDimensions:
    height: float
    base_diameter: float
    taper_ratio: float = 0.77

    def __post_init__(self):
        if any(dim <= 0 for dim in [self.height, self.base_diameter]):
            raise ValueError("Dimensions must be positive")
        if not 0 < self.taper_ratio <= 1:
            raise ValueError("Taper ratio must be between 0 and 1")


# ── Analyzer ─────────────────────────────────────────────────────

class ColumnAnalyzer:
    def __init__(self, dimensions: ColumnDimensions, material: Material = Material.MARBLE):
        self.dimensions = dimensions
        self.material = material

    def _base_radius(self):
        return self.dimensions.base_diameter / 2

    def _top_radius(self):
        return self._base_radius() * self.dimensions.taper_ratio

    def _volume(self):
        r1, r2, h = self._base_radius(), self._top_radius(), self.dimensions.height
        return (math.pi * h / 3) * (r1**2 + r2**2 + r1 * r2)

    def _geometric_moment(self, radius):
        return math.pi * radius**4 / 4

    def analyze(self) -> Dict:
        r1   = self._base_radius()
        r2   = self._top_radius()
        r_avg = (r1 + r2) / 2
        vol  = self._volume()
        mass = vol * self.material.density

        return {
            'material_name':         self.material.description,
            'material_density':      self.material.density,
            'height':                round(self.dimensions.height, 4),
            'base_diameter':         round(self.dimensions.base_diameter, 4),
            'top_diameter':          round(r2 * 2, 4),
            'taper_ratio':           round(self.dimensions.taper_ratio, 4),
            'volume':                round(vol, 4),
            'mass':                  round(mass, 2),
            'geometric_moment_base': round(self._geometric_moment(r1), 6),
            'mass_moment_base':      round(self._geometric_moment(r1) * self.material.density, 3),
            'geometric_moment_avg':  round(self._geometric_moment(r_avg), 6),
            'mass_moment_avg':       round(self._geometric_moment(r_avg) * self.material.density, 3),
        }
MATERIAL_CHOICES = [(m.name, m.value[1]) for m in Material]

def homepage(request):
    results = None
    errors = {}
    values = {
        'height': '10.43',
        'base_diameter': '1.90',
        'taper_ratio': '0.77',
        'material': 'MARBLE',
    }

    if request.method == 'POST':
        values = {
            'height': request.POST.get('height', ''),
            'base_diameter': request.POST.get('base_diameter', ''),
            'taper_ratio': request.POST.get('taper_ratio', ''),
            'material': request.POST.get('material', 'MARBLE'),
        }

        # Validate + parse
        try:
            height = float(values['height'])
            base_diameter = float(values['base_diameter'])
            taper_ratio = float(values['taper_ratio'])
            material = Material[values['material']]

            dims = ColumnDimensions(height, base_diameter, taper_ratio)
            analyzer = ColumnAnalyzer(dims, material)
            results = analyzer.analyze()

        except (ValueError, KeyError) as e:
            errors['general'] = str(e)
    return render(request, 'columndimensioncalculatorapp/homepage.html',{
        'results': results,
        'errors': errors,
        'values': values,
        'material_choices': MATERIAL_CHOICES,
    })
