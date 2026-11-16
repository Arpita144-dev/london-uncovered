-- ============================================================
-- LONDON UNCOVERED - Database Schema and Sample Data
-- Database: london_uncovered
-- ============================================================

CREATE DATABASE IF NOT EXISTS london_uncovered
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE london_uncovered;

-- ============================================================
-- TABLE: users
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    user_id    INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(150) NOT NULL UNIQUE,
    password   VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- TABLE: attractions
-- ============================================================
CREATE TABLE IF NOT EXISTS attractions (
    attraction_id INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(200) NOT NULL,
    description   TEXT,
    location      VARCHAR(300),
    entry_fee     VARCHAR(100)
) ENGINE=InnoDB;

-- ============================================================
-- TABLE: restaurants
-- ============================================================
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(200) NOT NULL,
    cuisine       VARCHAR(100),
    location      VARCHAR(300),
    price_range   VARCHAR(100)
) ENGINE=InnoDB;

-- ============================================================
-- TABLE: hotels
-- ============================================================
CREATE TABLE IF NOT EXISTS hotels (
    hotel_id       INT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(200) NOT NULL,
    location       VARCHAR(300),
    price_per_night VARCHAR(100),
    description    TEXT
) ENGINE=InnoDB;

-- ============================================================
-- TABLE: trips
-- ============================================================
CREATE TABLE IF NOT EXISTS trips (
    trip_id    INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT NOT NULL,
    trip_name  VARCHAR(200) NOT NULL,
    start_date DATE,
    end_date   DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_trips_user FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- TABLE: trip_attractions
-- ============================================================
CREATE TABLE IF NOT EXISTS trip_attractions (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    trip_id       INT NOT NULL,
    attraction_id INT NOT NULL,
    CONSTRAINT fk_ta_trip       FOREIGN KEY (trip_id)
        REFERENCES trips(trip_id) ON DELETE CASCADE,
    CONSTRAINT fk_ta_attraction FOREIGN KEY (attraction_id)
        REFERENCES attractions(attraction_id) ON DELETE CASCADE,
    CONSTRAINT uq_trip_attraction UNIQUE (trip_id, attraction_id)
) ENGINE=InnoDB;

-- ============================================================
-- TABLE: favourites
-- ============================================================
CREATE TABLE IF NOT EXISTS favourites (
    favourite_id  INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT NOT NULL,
    attraction_id INT NOT NULL,
    added_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fav_user       FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_fav_attraction FOREIGN KEY (attraction_id)
        REFERENCES attractions(attraction_id) ON DELETE CASCADE,
    CONSTRAINT uq_user_attraction UNIQUE (user_id, attraction_id)
) ENGINE=InnoDB;

-- ============================================================
-- SAMPLE DATA: attractions (10 records)
-- ============================================================
INSERT INTO attractions (name, description, location, entry_fee) VALUES
('Big Ben',
 'Big Ben is the nickname for the Great Bell of the striking clock at the north end of the Palace of Westminster. It is one of the most recognisable symbols of the United Kingdom and is often seen as a symbol of London. The clock tower was completed in 1859 and stands 96 metres tall.',
 'Westminster, London SW1A 0AA',
 'Free (exterior view)'),

('London Eye',
 'The London Eye is a giant Ferris wheel situated on the South Bank of the River Thames in London. It was constructed between 1996 and 1999 and has become one of the most popular paid tourist attractions in the United Kingdom. Each rotation takes approximately 30 minutes, offering stunning panoramic views of the city.',
 'Riverside Building, County Hall, London SE1 7PB',
 'From £27.00 (Adult)'),

('Tower Bridge',
 'Tower Bridge is a combined bascule and suspension bridge in London, built between 1886 and 1894. It crosses the River Thames close to the Tower of London and has become an iconic symbol of London. Visitors can walk across the high-level glass-floored walkways 42 metres above the river.',
 'Tower Bridge Rd, London SE1 2UP',
 'From £11.40 (Adult)'),

('Buckingham Palace',
 'Buckingham Palace is the London residence and administrative headquarters of the monarch of the United Kingdom. Acquired by King George III in 1761, it has been the official London residence of the British sovereign since 1837. The State Rooms are open to visitors during the summer months.',
 'Westminster, London SW1A 1AA',
 'From £30.00 (State Rooms, seasonal)'),

('British Museum',
 'The British Museum is a public institution dedicated to human history, art and culture. Its permanent collection of eight million works is among the largest and most comprehensive in existence, documenting the story of human culture from its beginnings to the present. Entry to the main collection is free.',
 'Great Russell St, London WC1B 3DG',
 'Free (main collection)'),

('Hyde Park',
 'Hyde Park is a major Royal Park in central London. It covers 142 hectares in the City of Westminster and is one of the largest parks in central London. It is the site of the famous Speakers Corner, the Serpentine Lake, and was the location of the Great Exhibition of 1851.',
 'London W2 2UH',
 'Free'),

('Tower of London',
 'The Tower of London, officially His Majesty''s Royal Palace and Fortress of the Tower of London, is a historic castle on the north bank of the River Thames in central London. The castle was founded in 1066. It houses the Crown Jewels of England and has served as a royal palace, prison, and place of execution.',
 'London EC3N 4AB',
 'From £29.90 (Adult)'),

('Tate Modern',
 'Tate Modern is an art gallery located in the former Bankside Power Station in Southwark, London. It is part of the Tate network of galleries and houses the Tate''s collection of international modern and contemporary art. It has been described as the world''s most visited gallery of modern and contemporary art.',
 'Bankside, London SE1 9TG',
 'Free (permanent collection)'),

('National Gallery',
 'The National Gallery is an art museum in Trafalgar Square in the City of Westminster, in central London. Founded in 1824, it houses a collection of over 2,300 paintings dating from the mid-13th century to 1900. The gallery is free to enter though charges apply for some temporary exhibitions.',
 'Trafalgar Square, London WC2N 5DN',
 'Free (permanent collection)'),

('Greenwich Royal Observatory',
 'The Royal Observatory Greenwich sits atop a hill in Greenwich Park overlooking the River Thames. It is the home of Greenwich Mean Time (GMT) and the Prime Meridian of the world. Visitors can stand on the meridian line and explore exhibits about astronomy and the history of navigation.',
 'Blackheath Ave, London SE10 8XJ',
 'From £18.00 (Adult)');

-- ============================================================
-- SAMPLE DATA: restaurants (6 records)
-- ============================================================
INSERT INTO restaurants (name, cuisine, location, price_range) VALUES
('The Ivy',
 'Modern British',
 '1-5 West St, London WC2H 9NQ',
 '££££ (£40–£80 per person)'),

('Dishoom',
 'Indian / Bombay Café',
 '12 Upper St Martin''s Lane, London WC2H 9FB',
 '££ (£20–£35 per person)'),

('Sketch London',
 'French / Contemporary European',
 '9 Conduit St, London W1S 2XG',
 '£££££ (£60–£120 per person)'),

('The Ledbury',
 'Modern European / Fine Dining',
 '127 Ledbury Rd, London W11 2AQ',
 '£££££ (£80–£150 per person)'),

('Flat Iron',
 'American Steakhouse',
 '17 Beak St, London W1F 9RW',
 '££ (£15–£30 per person)'),

('Ottolenghi',
 'Mediterranean / Middle Eastern',
 '287 Upper St, London N1 2TZ',
 '£££ (£25–£50 per person)');

-- ============================================================
-- SAMPLE DATA: hotels (6 records)
-- ============================================================
INSERT INTO hotels (name, location, price_per_night, description) VALUES
('The Ritz London',
 '150 Piccadilly, London W1J 9BR',
 'From £600 per night',
 'The Ritz London is a historic five-star hotel in the St. James''s district of London. Opened in 1906 by César Ritz, it offers 136 luxurious guest rooms and suites decorated in the Louis XVI style with stunning views of Green Park. Home to the famous Ritz Restaurant and Palm Court afternoon tea.'),

('Premier Inn London City',
 '1 Mansell St, London E1 8AL',
 'From £90 per night',
 'A budget-friendly hotel located in the heart of the City of London, within walking distance of Tower Bridge and the Tower of London. All rooms feature the famous Premier Inn Hypnos beds, en-suite bathroom, and free Wi-Fi. An excellent value option for travellers.'),

('The Savoy',
 'Strand, London WC2R 0EZ',
 'From £450 per night',
 'The Savoy is a luxury hotel situated in the Strand in London. Opened in 1889, it was the first luxury hotel in Britain and has hosted numerous celebrities and royalty. It offers 267 rooms and suites featuring Art Deco or Edwardian décor, along with the famous American Bar.'),

('Travelodge London Central City Road',
 '1 City Rd, London EC1Y 1AE',
 'From £60 per night',
 'An affordable hotel in the vibrant area of Old Street, close to Shoreditch and the City. Ideal for travellers on a budget who want good connectivity and central location. Rooms are clean, comfortable, and functional with modern amenities.'),

('Shangri-La The Shard',
 '31 St Thomas St, London SE1 9QU',
 'From £350 per night',
 'Located on floors 34 to 52 of The Shard, Europe''s tallest building, Shangri-La offers 202 rooms and suites with breathtaking panoramic views of London. Features the TĪNG restaurant and lounge, an infinity-edge pool, and world-class spa facilities.'),

('Hub by Premier Inn London Kings Cross',
 '10–18 York Way, London N1 9AA',
 'From £75 per night',
 'A modern, smart hotel situated minutes from Kings Cross and St Pancras International stations. Compact, cleverly designed rooms with adjustable lighting and smart TVs. Perfect for travellers who value location and connectivity at a great price.');
