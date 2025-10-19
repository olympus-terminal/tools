# High Data-Density Journal Figure Protocol

## Overview
This protocol defines standards for creating publication-quality, high-information-density figures suitable for high-impact journals (Nature, Science, Cell, PNAS).

## Core Principles

### 1. Information Density
- **Maximize data per pixel** - Every pixel should convey information
- **Multiple data layers** - Combine heatmaps, dendrograms, tracks, and annotations
- **No wasted space** - Minimal margins, tight layouts

### 2. Size Standards
- **Panel size**: 3.5-7 inches (89-178mm) width for single/double column
- **Full page**: A4 (8.27 × 11.69 inches)
- **Aspect ratios**: Optimize for scientific journals

### 3. Typography
- **ALL text**: 6pt Arial
- **Base font size**: 6pt
- **Font family**: Arial
- **Tick labels**: 6pt
- **Axis labels**: 6pt
- **Titles**: 6pt Bold
- **Legend**: 6pt
- **TrueType embedding**: PDF fonttype 42 for Illustrator compatibility

### 4. Color Schemes

#### For Abundance/Expression Data
```python
# Blackbody-inspired (black→red→orange→yellow)
colors = [
    (1.0, 1.0, 1.0),    # White for NaN/zero
    (0.95, 0.95, 0.95), # Very light gray
    (0.1, 0.1, 0.1),    # Near black
    (0.4, 0.0, 0.0),    # Dark red
    (0.7, 0.0, 0.0),    # Red
    (0.9, 0.2, 0.0),    # Orange-red
    (1.0, 0.5, 0.0),    # Orange
    (1.0, 0.7, 0.0),    # Yellow-orange
    (1.0, 0.9, 0.2),    # Yellow
]
```

#### For Correlations/Diverging Data
```python
# Blue-white-red diverging
colors = [
    (0.0, 0.3, 0.7),    # Deep blue (negative)
    (0.3, 0.5, 0.9),    # Medium blue
    (0.7, 0.8, 0.95),   # Light blue
    (0.95, 0.95, 0.95), # Near white (zero)
    (0.95, 0.8, 0.7),   # Light red
    (0.9, 0.4, 0.3),    # Medium red
    (0.7, 0.1, 0.1),    # Deep red (positive)
]
```

### 5. Technical Settings

```python
import matplotlib as mpl

# CRITICAL: Journal compatibility
mpl.rcParams['pdf.fonttype'] = 42  # TrueType fonts in PDF
mpl.rcParams['ps.fonttype'] = 42   # TrueType fonts in PostScript
mpl.rcParams['svg.fonttype'] = 'none'  # Embed fonts in SVG

# Font configuration - ALL 6pt Arial
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
mpl.rcParams['font.size'] = 6
mpl.rcParams['axes.labelsize'] = 6
mpl.rcParams['axes.titlesize'] = 6
mpl.rcParams['xtick.labelsize'] = 6
mpl.rcParams['ytick.labelsize'] = 6
mpl.rcParams['legend.fontsize'] = 6

# Line weights (always 0.25pt for publication quality)
mpl.rcParams['axes.linewidth'] = 0.25
mpl.rcParams['xtick.major.width'] = 0.25
mpl.rcParams['ytick.major.width'] = 0.25
mpl.rcParams['xtick.major.size'] = 2
mpl.rcParams['ytick.major.size'] = 2

# Minimal padding
mpl.rcParams['axes.labelpad'] = 1
mpl.rcParams['xtick.major.pad'] = 1
mpl.rcParams['ytick.major.pad'] = 1
```

## Figure Components

### 1. Complex Grid Layouts
```python
import matplotlib.gridspec as gridspec

# Multi-panel with varied ratios
gs = gridspec.GridSpec(6, 5, figure=fig,
                      height_ratios=[0.5, 0.8, 0.3, 4, 0.2, 0.3],
                      width_ratios=[0.15, 0.5, 3, 0.3, 0.15],
                      hspace=0.02,  # Minimal spacing
                      wspace=0.02)
```

### 2. Data Tracks (Top/Bottom)
- **Environmental variables**: Normalized heatmap strips
- **Sample metadata**: Colored bars for categories
- **Statistics**: Histogram distributions

### 3. Side Panels
- **Dendrograms**: Hierarchical clustering trees
- **Bar charts**: Correlation coefficients, p-values
- **Annotations**: Gene/protein names (abbreviated)

### 4. Main Heatmap
- **Data transformation**: Log2(x+1) for abundance
- **Missing values**: Always white
- **Grid lines**: Subtle (0.2 alpha) every 5-10 rows

## Implementation Checklist

### Pre-figure Preparation
- [ ] Load all data with proper dtypes
- [ ] Handle missing values explicitly
- [ ] Normalize/transform as needed
- [ ] Perform clustering analysis

### Figure Creation
- [ ] Set matplotlib rcParams
- [ ] Create figure with correct size
- [ ] Build complex grid layout
- [ ] Add dendrograms (if clustered)
- [ ] Add environmental/metadata tracks
- [ ] Plot main heatmap
- [ ] Add statistical side panels
- [ ] Add minimal colorbars
- [ ] Add concise labels

### Quality Control
- [ ] No overlapping text
- [ ] All fonts = 6pt Arial
- [ ] Transparent background
- [ ] NaN values shown as white
- [ ] Line weights = 0.25pt
- [ ] No subscript/superscript unicode

### Export Settings
```python
# ALWAYS use vector formats (PDF + SVG) - NO PNG raster files
# ALWAYS use transparent backgrounds - NOT white

# Save vector formats only
for fmt in ['pdf', 'svg']:
    filename = f'figures/figure_name.{fmt}'
    fig.savefig(filename, format=fmt,
               bbox_inches='tight',
               transparent=True,  # CRITICAL: transparent background
               edgecolor='none')
```

**IMPORTANT NOTES:**
- **Vector graphics only**: Use PDF and SVG formats exclusively
- **NO PNG files**: Raster graphics are not acceptable for publication figures
- **Transparent backgrounds**: Always use `transparent=True`, never `facecolor='white'`
- **Illustrator compatibility**: TrueType fonts (fonttype 42) ensure editability

## Example Features from highdensity_salinity_v3

### Successful Elements
1. **Six-track layout**: Dendrograms + env vars + taxa + heatmap + stats + legend
2. **29 PFAMs × 134 samples**: Full dataset, not subsampled
3. **Dual clustering**: Both rows and columns organized
4. **Statistical overlay**: Significance markers on correlation matrix
5. **Color legends**: Integrated as data tracks
6. **Abbreviated labels**: "2119" instead of "PF02119"

### Space-Saving Techniques
1. **Shared axes**: Multiple panels use same x/y coordinates
2. **Inline legends**: Color bars as data tracks
3. **Sparse labeling**: Every 5th PFAM labeled
4. **Compact colorbars**: 0.008 width fraction
5. **Merged annotations**: Taxa shown as colored bar, not text

## Common Pitfalls to Avoid

### Typography Issues
- ❌ Using fonts other than 6pt Arial
- ❌ Unicode subscripts (₁₂₃)
- ❌ **OVERLAPPING TEXT** - This is the #1 rejection reason
- ❌ Text overlapping with plot elements (axes, bars, points)
- ❌ Variable text sizes within a figure
- ✅ Use "Log2" not "Log₂"
- ✅ Rotate labels 45° if needed
- ✅ Abbreviate aggressively
- ✅ **Check every text element for overlap**
- ✅ Use `adjustText` library for automatic label placement
- ✅ ALL text must be 6pt - NO exceptions

### Layout Problems
- ❌ Large margins/padding
- ❌ Separate legend boxes
- ❌ Empty space
- ❌ Low data-to-ink ratio
- ❌ Sparse plots with lots of whitespace
- ✅ Tight layouts (hspace/wspace < 0.1)
- ✅ Integrated legends
- ✅ Fill entire figure area
- ✅ **Maximize data density** - show as much information as possible

### Color Issues
- ❌ Default matplotlib colors
- ❌ Rainbow colormaps
- ❌ Non-white NaN values
- ✅ Perceptually uniform gradients
- ✅ Colorblind-safe palettes
- ✅ White for missing data

## Validation Steps

### CRITICAL Pre-Submission Checks (MUST PASS ALL):

1. **Text Overlap Check**:
   - Zoom to 400% and inspect EVERY text element
   - NO text overlapping with other text
   - NO text overlapping with plot elements
   - Use white/transparent bounding boxes if absolutely necessary

2. **Font Size Check**:
   - ALL text must be exactly 6pt Arial
   - Measure in Illustrator/Inkscape to verify
   - NO variation in font sizes

3. **Data Density Check**:
   - Calculate data-to-ink ratio
   - Aim for >70% of figure area showing data
   - Remove all unnecessary whitespace
   - Increase number of data points shown

4. **Zoom test**: Zoom to 400% - text should remain crisp and non-overlapping

5. **Print test**: Print at actual size - all elements visible and separated

6. **Grayscale test**: Convert to B&W - patterns still distinguishable

7. **Illustrator test**: Open PDF - all fonts editable and 6pt

## References
- Nature figure guidelines: https://www.nature.com/nature/for-authors/final-submission
- Science figure specs: https://www.science.org/content/page/instructions-preparing-initial-manuscript
- Cell figure guidelines: https://www.cell.com/figure-guidelines

## Version History
- v1.0 (2024): Initial protocol based on highdensity_salinity_v3.py success
- v1.1 (2025-10-18): Standardized ALL fonts to 6pt Arial
- v1.2 (2025-10-18): Added strict no-overlap rules, data density requirements, mandatory validation checks

---

*Remember: Every pixel should justify its existence. If it doesn't convey information, remove it# High Data-Density Journal Figure Protocol

## Overview
This protocol defines standards for creating publication-quality, high-information-density figures suitable for high-impact journals (Nature, Science, Cell, PNAS).

## Core Principles

### 1. Information Density
- **Maximize data per pixel** - Every pixel should convey information
- **Multiple data layers** - Combine heatmaps, dendrograms, tracks, and annotations
- **No wasted space** - Minimal margins, tight layouts

### 2. Size Standards
- **Panel size**: 3.5-7 inches (89-178mm) width for single/double column
- **Full page**: A4 (8.27 × 11.69 inches)
- **Aspect ratios**: Optimize for scientific journals

### 3. Typography
- **ALL text**: 6pt Arial
- **Base font size**: 6pt
- **Font family**: Arial
- **Tick labels**: 6pt
- **Axis labels**: 6pt
- **Titles**: 6pt Bold
- **Legend**: 6pt
- **TrueType embedding**: PDF fonttype 42 for Illustrator compatibility

### 4. Color Schemes

#### For Abundance/Expression Data
```python
# Blackbody-inspired (black→red→orange→yellow)
colors = [
    (1.0, 1.0, 1.0),    # White for NaN/zero
    (0.95, 0.95, 0.95), # Very light gray
    (0.1, 0.1, 0.1),    # Near black
    (0.4, 0.0, 0.0),    # Dark red
    (0.7, 0.0, 0.0),    # Red
    (0.9, 0.2, 0.0),    # Orange-red
    (1.0, 0.5, 0.0),    # Orange
    (1.0, 0.7, 0.0),    # Yellow-orange
    (1.0, 0.9, 0.2),    # Yellow
]
```

#### For Correlations/Diverging Data
```python
# Blue-white-red diverging
colors = [
    (0.0, 0.3, 0.7),    # Deep blue (negative)
    (0.3, 0.5, 0.9),    # Medium blue
    (0.7, 0.8, 0.95),   # Light blue
    (0.95, 0.95, 0.95), # Near white (zero)
    (0.95, 0.8, 0.7),   # Light red
    (0.9, 0.4, 0.3),    # Medium red
    (0.7, 0.1, 0.1),    # Deep red (positive)
]
```

### 5. Technical Settings

```python
import matplotlib as mpl

# CRITICAL: Journal compatibility
mpl.rcParams['pdf.fonttype'] = 42  # TrueType fonts in PDF
mpl.rcParams['ps.fonttype'] = 42   # TrueType fonts in PostScript
mpl.rcParams['svg.fonttype'] = 'none'  # Embed fonts in SVG

# Font configuration - ALL 6pt Arial
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
mpl.rcParams['font.size'] = 6
mpl.rcParams['axes.labelsize'] = 6
mpl.rcParams['axes.titlesize'] = 6
mpl.rcParams['xtick.labelsize'] = 6
mpl.rcParams['ytick.labelsize'] = 6
mpl.rcParams['legend.fontsize'] = 6

# Line weights (always 0.25pt for publication quality)
mpl.rcParams['axes.linewidth'] = 0.25
mpl.rcParams['xtick.major.width'] = 0.25
mpl.rcParams['ytick.major.width'] = 0.25
mpl.rcParams['xtick.major.size'] = 2
mpl.rcParams['ytick.major.size'] = 2

# Minimal padding
mpl.rcParams['axes.labelpad'] = 1
mpl.rcParams['xtick.major.pad'] = 1
mpl.rcParams['ytick.major.pad'] = 1
```

## Figure Components

### 1. Complex Grid Layouts
```python
import matplotlib.gridspec as gridspec

# Multi-panel with varied ratios
gs = gridspec.GridSpec(6, 5, figure=fig,
                      height_ratios=[0.5, 0.8, 0.3, 4, 0.2, 0.3],
                      width_ratios=[0.15, 0.5, 3, 0.3, 0.15],
                      hspace=0.02,  # Minimal spacing
                      wspace=0.02)
```

### 2. Data Tracks (Top/Bottom)
- **Environmental variables**: Normalized heatmap strips
- **Sample metadata**: Colored bars for categories
- **Statistics**: Histogram distributions

### 3. Side Panels
- **Dendrograms**: Hierarchical clustering trees
- **Bar charts**: Correlation coefficients, p-values
- **Annotations**: Gene/protein names (abbreviated)

### 4. Main Heatmap
- **Data transformation**: Log2(x+1) for abundance
- **Missing values**: Always white
- **Grid lines**: Subtle (0.2 alpha) every 5-10 rows

## Implementation Checklist

### Pre-figure Preparation
- [ ] Load all data with proper dtypes
- [ ] Handle missing values explicitly
- [ ] Normalize/transform as needed
- [ ] Perform clustering analysis

### Figure Creation
- [ ] Set matplotlib rcParams
- [ ] Create figure with correct size
- [ ] Build complex grid layout
- [ ] Add dendrograms (if clustered)
- [ ] Add environmental/metadata tracks
- [ ] Plot main heatmap
- [ ] Add statistical side panels
- [ ] Add minimal colorbars
- [ ] Add concise labels

### Quality Control
- [ ] No overlapping text
- [ ] All fonts = 6pt Arial
- [ ] Transparent background
- [ ] NaN values shown as white
- [ ] Line weights = 0.25pt
- [ ] No subscript/superscript unicode

### Export Settings
```python
# ALWAYS use vector formats (PDF + SVG) - NO PNG raster files
# ALWAYS use transparent backgrounds - NOT white

# Save vector formats only
for fmt in ['pdf', 'svg']:
    filename = f'figures/figure_name.{fmt}'
    fig.savefig(filename, format=fmt,
               bbox_inches='tight',
               transparent=True,  # CRITICAL: transparent background
               edgecolor='none')
```

**IMPORTANT NOTES:**
- **Vector graphics only**: Use PDF and SVG formats exclusively
- **NO PNG files**: Raster graphics are not acceptable for publication figures
- **Transparent backgrounds**: Always use `transparent=True`, never `facecolor='white'`
- **Illustrator compatibility**: TrueType fonts (fonttype 42) ensure editability

## Example Features from highdensity_salinity_v3

### Successful Elements
1. **Six-track layout**: Dendrograms + env vars + taxa + heatmap + stats + legend
2. **29 PFAMs × 134 samples**: Full dataset, not subsampled
3. **Dual clustering**: Both rows and columns organized
4. **Statistical overlay**: Significance markers on correlation matrix
5. **Color legends**: Integrated as data tracks
6. **Abbreviated labels**: "2119" instead of "PF02119"

### Space-Saving Techniques
1. **Shared axes**: Multiple panels use same x/y coordinates
2. **Inline legends**: Color bars as data tracks
3. **Sparse labeling**: Every 5th PFAM labeled
4. **Compact colorbars**: 0.008 width fraction
5. **Merged annotations**: Taxa shown as colored bar, not text

## Common Pitfalls to Avoid

### Typography Issues
- ❌ Using fonts other than 6pt Arial
- ❌ Unicode subscripts (₁₂₃)
- ❌ **OVERLAPPING TEXT** - This is the #1 rejection reason
- ❌ Text overlapping with plot elements (axes, bars, points)
- ❌ Variable text sizes within a figure
- ✅ Use "Log2" not "Log₂"
- ✅ Rotate labels 45° if needed
- ✅ Abbreviate aggressively
- ✅ **Check every text element for overlap**
- ✅ Use `adjustText` library for automatic label placement
- ✅ ALL text must be 6pt - NO exceptions

### Layout Problems
- ❌ Large margins/padding
- ❌ Separate legend boxes
- ❌ Empty space
- ❌ Low data-to-ink ratio
- ❌ Sparse plots with lots of whitespace
- ✅ Tight layouts (hspace/wspace < 0.1)
- ✅ Integrated legends
- ✅ Fill entire figure area
- ✅ **Maximize data density** - show as much information as possible

### Color Issues
- ❌ Default matplotlib colors
- ❌ Rainbow colormaps
- ❌ Non-white NaN values
- ✅ Perceptually uniform gradients
- ✅ Colorblind-safe palettes
- ✅ White for missing data

## Validation Steps

### CRITICAL Pre-Submission Checks (MUST PASS ALL):

1. **Text Overlap Check**:
   - Zoom to 400% and inspect EVERY text element
   - NO text overlapping with other text
   - NO text overlapping with plot elements
   - Use white/transparent bounding boxes if absolutely necessary

2. **Font Size Check**:
   - ALL text must be exactly 6pt Arial
   - Measure in Illustrator/Inkscape to verify
   - NO variation in font sizes

3. **Data Density Check**:
   - Calculate data-to-ink ratio
   - Aim for >70% of figure area showing data
   - Remove all unnecessary whitespace
   - Increase number of data points shown

4. **Zoom test**: Zoom to 400% - text should remain crisp and non-overlapping

5. **Print test**: Print at actual size - all elements visible and separated

6. **Grayscale test**: Convert to B&W - patterns still distinguishable

7. **Illustrator test**: Open PDF - all fonts editable and 6pt

## References
- Nature figure guidelines: https://www.nature.com/nature/for-authors/final-submission
- Science figure specs: https://www.science.org/content/page/instructions-preparing-initial-manuscript
- Cell figure guidelines: https://www.cell.com/figure-guidelines

## Version History
- v1.0 (2024): Initial protocol based on highdensity_salinity_v3.py success
- v1.1 (2025-10-18): Standardized ALL fonts to 6pt Arial
- v1.2 (2025-10-18): Added strict no-overlap rules, data density requirements, mandatory validation checks

---

*Remember: Every pixel should justify its existence. If it doesn't convey information, remove it
