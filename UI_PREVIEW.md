# UI Preview - Transactions Tab

## Overview

This document provides a visual description of the implemented Transactions tab in the Personal Finance Dashboard.

## Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  Personal Finance Dashboard                    [Upload] [Logout]    │
├─────────────────────────────────────────────────────────────────────┤
│  [Transactions] [Income] [Expenses] [Net Worth]                     │
│   ^^^^^^^^^^^                                                        │
│   Active Tab                                                         │
└─────────────────────────────────────────────────────────────────────┘
```

## Transactions Tab - With Data

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│  Transactions                                               [Refresh]│
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ Grocery Store Purchase                         -$45.67           ││
│  │ Whole Foods • [Groceries]                      Jan 15, 2024      ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ Electric Bill                                  -$120.00          ││
│  │ Power Company • [Utilities]                    Jan 14, 2024      ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ Monthly Salary                                 $5,000.00         ││
│  │ Tech Corp • [Salary]                           Jan 1, 2024       ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                       │
│                         [Load More]                                  │
│                   Showing 3 of 150 transactions                      │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Transactions Tab - Loading State

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│  Transactions                                               [Refresh]│
│                                                                       │
│                             ⟳                                        │
│                    Loading transactions...                           │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Transactions Tab - Empty State

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│  Transactions                                               [Refresh]│
│                                                                       │
│                             📄                                       │
│         No transactions to display yet.                              │
│         Upload a bank statement to get started.                      │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Transactions Tab - Error State

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│  Transactions                                               [Refresh]│
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ ⚠ API endpoint not configured. Please check your .env file.    ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                       │
│                             📄                                       │
│         No transactions to display yet.                              │
│         Upload a bank statement to get started.                      │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Transaction Card Details

Each transaction card displays:

1. **Main Line:**
   - **Left:** Transaction description (bold, dark text)
   - **Right:** Amount (colored - red for debit, green for credit)

2. **Meta Line:**
   - **Left:** Merchant name • Category badge (with gray background)
   - **Right:** Formatted date (e.g., "Jan 15, 2024")

## Visual Design Elements

### Colors
- **Debit Amounts:** Red (#ef4444) - indicates money spent
- **Credit Amounts:** Green (#10b981) - indicates money received
- **Primary Color:** Purple gradient (#667eea to #764ba2) for buttons
- **Text Colors:**
  - Primary: Dark gray (#333)
  - Secondary: Medium gray (#666)
  - Tertiary: Light gray (#999)

### Typography
- **Transaction Description:** 16px, medium weight (500)
- **Amount:** 18px, semi-bold (600)
- **Metadata:** 13px, normal weight
- **Category Badge:** 13px, medium weight (500)

### Spacing & Layout
- **Card Padding:** 16px
- **Card Gap:** 12px between cards
- **Border:** 1px solid light gray (#e5e7eb)
- **Border Radius:** 8px for rounded corners
- **Hover Effect:** Purple border with subtle shadow

### Interactive Elements

#### Refresh Button
- Icon-only button with spinning refresh icon
- Located in the top-right corner
- Spins when loading
- Disabled during loading (grayed out)

#### Load More Button
- Centered below transaction list
- Outlined style (white background, purple border)
- Hover effect: fills with purple background
- Shows "Loading..." text when fetching more data
- Disabled during loading

### Responsive Design

#### Desktop (>768px)
- Transaction cards: Full width with side-by-side layout
- Amount and date aligned to the right
- Description and metadata aligned to the left

#### Mobile (<768px)
- Transaction cards: Stack vertically
- Amount and date below description
- All text left-aligned
- Reduced padding and font sizes

## User Interactions

### 1. Initial Load
- User signs in and navigates to Dashboard
- Transactions tab is selected by default
- Loading spinner appears
- Transactions fetch from API
- List displays sorted by date (newest first)

### 2. Refresh
- User clicks refresh button (⟳)
- Button icon spins
- Transaction list is reloaded from beginning
- List updates with latest data

### 3. Load More
- User scrolls to bottom and clicks "Load More"
- Button text changes to "Loading..."
- Next page of transactions is fetched
- New transactions are appended to list
- Pagination counter updates
- Button re-enables when ready

### 4. Error Handling
- If API not configured: Shows error message at top
- If network error: Shows error message
- Error can be dismissed by refreshing
- Placeholder state remains visible below error

## Accessibility Features

- **Semantic HTML:** Proper button and list elements
- **Keyboard Navigation:** All buttons are keyboard accessible
- **Loading States:** Clear visual indicators
- **Error Messages:** Descriptive error text
- **Color Contrast:** WCAG AA compliant text colors
- **Focus Indicators:** Visible focus states on interactive elements

## Technical Implementation Notes

### Data Flow
1. Dashboard component mounts
2. `useEffect` triggers when "transactions" tab is active
3. `fetchTransactions()` is called
4. API service fetches data with JWT token
5. Transactions are sorted by date
6. State updates trigger re-render
7. UI displays transactions

### State Management
- `transactions` - Array of transaction objects
- `loading` - Boolean for loading state
- `error` - String for error message (or null)
- `pagination` - Object with limit, offset, total
- `activeTab` - String for current tab

### Performance Considerations
- Memoized fetch function with `useCallback`
- Proper dependency array in `useEffect`
- Minimal re-renders
- Efficient sorting algorithm
- No unnecessary API calls

## Example Transaction Data Structure

```javascript
{
  id: "txn_001",
  userId: "user_123",
  date: "2024-01-15",
  amount: -45.67,
  description: "Grocery Store Purchase",
  category: "groceries",
  merchant: "Whole Foods",
  type: "debit",
  accountId: "acc_001",
  createdAt: "2024-01-16T10:30:00Z",
  updatedAt: "2024-01-16T10:30:00Z"
}
```

## API Integration

### Endpoint
```
GET /v1/transactions?limit=50&offset=0
```

### Headers
```
Authorization: Bearer {JWT_ID_TOKEN}
Content-Type: application/json
```

### Response
```json
{
  "data": [...],
  "pagination": {
    "limit": 50,
    "offset": 0,
    "total": 150
  }
}
```

## Next Steps for Testing

To see this UI in action:

1. **Set up AWS Resources** (follow `AWS_RESOURCES_SETUP.md`)
2. **Configure Environment Variables** (copy `.env.example` to `.env`)
3. **Start the Application**
   ```bash
   cd frontend
   npm install
   npm start
   ```
4. **Sign In** with Cognito user
5. **Navigate to Transactions Tab**
6. **Verify** all features work as expected

## Summary

The Transactions tab provides a clean, intuitive interface for viewing financial transactions with:
- ✅ Clear visual hierarchy
- ✅ Color-coded amounts
- ✅ Easy-to-read formatting
- ✅ Smooth loading states
- ✅ Helpful error messages
- ✅ Pagination support
- ✅ Responsive design
- ✅ Accessibility features

The implementation follows modern React best practices and provides a solid foundation for future enhancements.
