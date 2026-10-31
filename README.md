# LONDON UNCOVERED — A VISUAL LONDON TRAVEL GUIDE

> **Discover London, One Experience at a Time.**  
> *A premium travel magazine transformed into an interactive desktop application.*

---

## 🇬🇧 1. Project Overview

**London Uncovered** is a desktop travel guide application focused exclusively on London, England. Developed as an interactive frontend showcase, the application combines a sophisticated editorial aesthetic with real-time destination discovery, rich London photography, interactive category filtering, and a personalised multi-day itinerary planner.

### Visual Design & Palette
Designed to evoke the elegance of a luxury print travel publication:
- **Background Cream:** `#F8F5EF` — Soft, glare-free magazine paper background
- **Deep Navy:** `#142B3B` — Bold structural navigation and hero features
- **Burgundy:** `#762E3D` — Highlights, selected category chips, and calls to action
- **Muted Gold:** `#C5A46D` — Decorative accents, tags, and rating emblems
- **Light Grey & White:** `#E9E5DE` / `#FFFFFF` — Elevated cards and borders
- **Dark Text:** `#292929` — High-contrast typography

---

## 🏛️ 2. Key Features

### 1. Home Dashboard
- **Photographic Hero Panel:** Features London's iconic skyline and Westminster with direct CTA buttons to *Explore London* and *Plan My Trip*.
- **Explore The City:** Featured destination cards for **Big Ben**, **Tower Bridge**, **Buckingham Palace**, and **The London Eye**.
- **Find Your London:** Six curated thematic pathways (Iconic Landmarks, Hidden Gems, Food & Markets, History & Museums, Parks & Gardens, Shopping).

### 2. Destination Discovery (Explore London)
- Curated collection of **20+ London destinations**, including:
  1. Big Ben & Houses of Parliament
  2. Tower Bridge
  3. Buckingham Palace
  4. The London Eye
  5. Westminster Abbey
  6. St Paul's Cathedral
  7. Natural History Museum
  8. British Museum
  9. Hyde Park & Kensington Gardens
  10. Covent Garden
  11. Borough Market
  12. Camden Market & Regent's Canal
  13. Notting Hill & Portobello Road
  14. Greenwich & Royal Observatory
  15. Leadenhall Market
  16. Little Venice
  17. Neal's Yard
  18. Hampstead Heath & Parliament Hill
  19. Soho & Chinatown
  20. Shoreditch & Brick Lane
- **Live Search Bar:** Search instantly by name, neighbourhood, category, or keywords.
- **Category Filter Chips:** Filter dynamically by *All*, *Landmarks*, *Museums*, *Parks*, *Food & Markets*, *Shopping*, or *Hidden Gems*.
- **Interactive Cards:** Features high-resolution photography, neighbourhood badges, estimated visit durations, details buttons, and persistent heart-shaped favourite toggles.

### 3. Dedicated Destination Details
- Magazine-style dedicated panel with large photography.
- Detailed editorial background, **Why It Is Famous**, **Did You Know?** facts, **Things To Do**, and **Practical Visitor Tips** (nearest tube stations, ideal visiting times).
- **"Add to My Trip"** button: Directly queues the destination into your personalized itinerary generator.
- **"Save to Favourites"** button: Persists the place to local storage.

### 4. Beyond the Postcards (Hidden Gems)
- Distinct editorial layout featuring secret courtyards, quiet canals, and panoramic viewpoints:
  - **Neal's Yard** (Seven Dials, Covent Garden)
  - **Little Venice** (Regent's Canal, Maida Vale)
  - **Leadenhall Market** (Historic Victorian City Arcade & Harry Potter filming site)
  - **Hampstead Heath & Parliament Hill** (Wild woodland with protected skyline views)

### 5. Curated London Experiences
- Four immersive travel pillars:
  - **Food & Cafés:** Street food stalls, traditional afternoon tea, Chinatown dim sum.
  - **Shopping & Markets:** Portobello antiques, Covent Garden Apple Market, Shoreditch vintage.
  - **Culture & Entertainment:** West End theatreland, free national museums, and royal pageantry.
  - **Scenic London:** Thames riverwalks, canal cruises, and royal park strolls.

### 6. London Neighbourhood Guide
- Dedicated discovery of 8 distinct London districts:
  - **Westminster** (Monumental & Regal)
  - **Covent Garden** (Theatrical & Bustling)
  - **Soho & Chinatown** (Bohemian & Electrifying)
  - **Notting Hill** (Pastel & Romantic)
  - **Camden Town** (Alternative & Vibrant)
  - **Greenwich** (Maritime & Grand)
  - **South Bank & Bankside** (Cultural & Panoramic)
  - **Shoreditch & East End** (Edgy & Artistic)
- Filter all destinations by neighbourhood with a single click.

### 7. Interactive Itinerary Planner
- **Step 1: Duration** — Choose 1, 2, 3, or 5 Days.
- **Step 2: Interests** — Multi-select from History, Museums, Food, Shopping, Parks, Photography, Hidden Gems, and Culture.
- **Step 3: Budget** — Budget-friendly, Balanced, or Premium.
- **Step 4: Pace** — Relaxed (2-3 stops/day), Balanced (3-4 stops/day), or Packed (5-6 stops/day).
- **Rule-Based Recommendation Engine:**
  - Clusters geographically nearby destinations to minimize travel time across London.
  - Prioritizes destinations hand-picked via "Add to My Trip".
  - Integrates suggested lunch and dinner breaks (e.g. Borough Market, Chinatown, afternoon tea).
  - Day-by-day tabs with timeline slots, visit durations, and visitor tips.
- **Controls & Export:**
  - **Save Itinerary:** Persists to `storage/saved_itineraries.json`.
  - **Saved Itineraries Drawer:** Review and reload previously saved trips.
  - **Add / Remove Destination:** Manually adjust any day's schedule.
  - **Print / HTML Export:** Generates a beautifully formatted, print-ready HTML travel document and opens it in your default browser.

### 8. Saved Places (Favourites)
- Persistent wishlist saved to `storage/favourites.json`.
- Favourites persist across app launches.
- Welcoming empty state guiding users back to discovery.

### 9. London Food Guide ("A Taste of London")
- Deep dive into traditional British classics, Afternoon Tea rituals, global street food markets, Chinatown dim sum, artisan bakeries, and covered food halls.

### 10. Practical Travel Tips
- Essential advice on the London Underground (Oyster vs Contactless daily caps, the "stand on the right" rule), walking distances, booking popular attractions in advance, free museum admissions, packing for London weather, bus hopper fares, and emergency numbers.

---

## 📂 3. Project Directory Structure

```text
london_uncovered/
├── main.py                     # Main application entry point and router
├── requirements.txt           # Python dependencies
├── README.md                  # Comprehensive documentation
├── assets/                    # 26 high-resolution local London photographs
│   ├── london_hero.jpg
│   ├── big_ben.jpg
│   ├── tower_bridge.jpg
│   ├── buckingham_palace.jpg
│   ├── london_eye.jpg
│   ├── westminster_abbey.jpg
│   ├── st_pauls.jpg
│   ├── natural_history_museum.jpg
│   ├── british_museum.jpg
│   ├── hyde_park.jpg
│   ├── covent_garden.jpg
│   ├── borough_market.jpg
│   ├── camden_market.jpg
│   ├── notting_hill.jpg
│   ├── greenwich.jpg
│   ├── leadenhall_market.jpg
│   ├── little_venice.jpg
│   ├── neals_yard.jpg
│   ├── hampstead_heath.jpg
│   ├── soho.jpg
│   ├── shoreditch.jpg
│   ├── south_bank.jpg
│   ├── afternoon_tea.jpg
│   ├── chinatown.jpg
│   ├── british_food.jpg
│   └── tube_transport.jpg
├── data/                      # Local JSON databases
│   ├── destinations.json      # 20 richly documented London destinations
│   ├── experiences.json       # 4 curated experience categories
│   ├── neighbourhoods.json    # 8 detailed London neighbourhoods
│   ├── food_guide.json        # 6 culinary categories & dishes
│   └── travel_tips.json       # 8 practical travel advice cards
├── storage/                   # Local persistent user storage
│   ├── favourites.json        # User saved destination IDs
│   └── saved_itineraries.json # Saved travel plans
├── app/
│   ├── config.py              # Brand colors, typography, paths
│   ├── data_manager.py        # Safe JSON loading, persistence & search
│   ├── image_manager.py       # Pillow cropping (ImageOps.fit) & fallbacks
│   ├── navigation.py          # Left persistent sidebar
│   ├── utils/
│   │   ├── download_assets.py     # Unsplash asset manager & fallback generator
│   │   └── itinerary_generator.py # Rule-based geo-clustering itinerary engine
│   └── views/
│       ├── home_view.py           # Home dashboard
│       ├── explore_view.py        # Destination discovery & search
│       ├── detail_view.py         # Magazine detail panel
│       ├── hidden_gems_view.py    # Asymmetric editorial layout
│       ├── experiences_view.py    # Experience showcase
│       ├── neighbourhood_view.py  # 8 neighbourhoods guide
│       ├── itinerary_view.py      # Interactive multi-step planner
│       ├── favourites_view.py     # Persistent favourites
│       ├── food_view.py           # "A Taste of London" food guide
│       └── travel_tips_view.py    # Tube and travel advice
```

---

## 🚀 4. Installation & Execution Instructions

### Prerequisites
- Python 3.10 or newer (tested on Python 3.14).
- Standard Tkinter support (included with standard Python installations on macOS and Windows).

### Step 1: Navigate to the Project Directory
```bash
cd /Users/arpita/.gemini/antigravity/scratch/london_uncovered
```

### Step 2: Install Dependencies
Install the required packages using pip:
```bash
pip3 install -r requirements.txt
```
*(Dependencies installed: `customtkinter`, `Pillow`, `darkdetect`)*

### Step 3: Run the Application
Launch the desktop application:
```bash
python3 main.py
```

---

## 🛡️ 5. Reliability & Offline Operation
- **Local Image Assets:** All 26 authentic London photographs are bundled locally in `assets/`.
- **Procedural Pillow Fallback:** In the event that an image file is deleted or inaccessible, `ImageManager` procedurally generates an elegant, branded editorial placeholder using Pillow's `ImageDraw` without crashing.
- **Distortion-Free Cropping:** Uses `ImageOps.fit` with high-quality Lanczos resampling so destination photographs are never stretched or squished.
- **Garbage-Collection Safe:** Keeps active references to `CTkImage` objects to prevent UI blanking.
- **Resilient Storage:** All JSON reads and writes handle missing directories or invalid files gracefully.

---

## 🎓 6. Academic / Project Notes
- Developed as a modern Python Desktop GUI project demonstrating:
  - CustomTkinter component hierarchies and custom styling.
  - Pillow image manipulation and responsive rendering.
  - Clean separation of concerns (Data Layer, Logic Layer, UI Views).
  - Interactive multi-criteria algorithmic itinerary generation.
