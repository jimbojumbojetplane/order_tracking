# Store Integration - Complete

## Summary

Successfully integrated store management from Notion database into the Cellcom Order Tracker application. Stores are now properly linked to orders, customers, and users.

## Changes Made

### 1. Database Models (`models.py`)

- **New `Store` Model**: 
  - Fields: `name`, `street`, `city`, `province`, `postal_code`, `latitude`, `longitude`, `is_active`
  - Relationships to `User` and `Order`
  - Helper properties: `full_address`, `display_name`

- **Updated `User` Model**:
  - Added `store_id` foreign key (optional) - reps can be assigned to stores

- **Updated `Order` Model**:
  - Added `store_id` foreign key (required)
  - Kept `store_location` string field for backwards compatibility (now auto-populated from store)

- **Updated `Customer` Model**:
  - Changed `preferred_store` (string) to `preferred_store_id` (foreign key to Store)

### 2. Store Data (`seed/stores_from_notion.json`)

- Extracted 47 store locations from Notion database
- Includes all fields: name, address, city, province, postal code, coordinates
- Ready for seeding into database

### 3. Seed Scripts

- **`seed/seed_stores.py`**: Imports stores from JSON file
- **Updated `seed/seed_customers.py`**: Now uses `preferred_store_id` instead of string
- **Updated `seed/seed_orders.py`**: Now uses Store objects instead of strings
- **Updated `init_db.py`**: Includes store seeding before other data

### 4. Order Entry Flow

- **Order Form (`templates/orders/new.html`)**:
  - Replaced text input with dropdown selection
  - Stores grouped by city/province
  - Auto-selects user's default store if assigned
  - Shows store name and street address in dropdown

- **Order Routes (`routes/orders.py`)**:
  - Validates store selection
  - Auto-populates `store_location` from selected store
  - Default store selection based on user's `store_id`

### 5. Store Management

- **New Routes (`routes/stores.py`)**:
  - `GET /stores` - List all stores with filtering by search and province
  - `GET /stores/<id>` - Store detail page with recent orders

- **Templates**:
  - `templates/stores/list.html` - Store listing with filters
  - `templates/stores/detail.html` - Individual store view with orders

- **Navigation**: Added "Stores" link to main navigation

### 6. Display Updates

- **Order List**: Shows store name and city instead of location string
- **Order Detail**: Shows full store address if store relationship exists
- **Customer Detail**: Shows preferred store name if set
- **Customer List**: Shows preferred store name

## Database Migration Required

⚠️ **Important**: The database schema has changed. You need to either:

### Option 1: Fresh Start (Recommended for Development)
```bash
# Delete existing database
rm instance/celldb.db

# Reinitialize with new schema
python3 init_db.py
```

### Option 2: Manual Migration (Production)
You'll need to:
1. Create the `stores` table
2. Add `store_id` column to `users` table
3. Add `store_id` column to `orders` table
4. Change `preferred_store` to `preferred_store_id` in `customers` table
5. Migrate existing data

## Next Steps

1. **Seed Stores**: After reinitializing database, stores will be automatically seeded
2. **Assign Users to Stores** (Optional): Update user records to assign them to default stores
3. **Test Order Entry**: Create a new order and verify store selection works

## Features

✅ Store selection dropdown in order form  
✅ Stores grouped by city for easy selection  
✅ Auto-select user's default store  
✅ Store filtering in order list  
✅ Store detail pages with order history  
✅ Store list with search and province filtering  
✅ Full address display on order details  

## Notes

- The `store_location` field is kept for backwards compatibility but is now auto-populated from the selected store
- Users can be assigned to stores (optional) - this will pre-select their store in the order form
- Customers can have a preferred store assigned (foreign key relationship)

