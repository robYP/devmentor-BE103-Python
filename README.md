# Event Notification System

A FastAPI-based web application for managing and triggering event notifications across multiple channels (Email, LINE) with multi-language support.

## Features

- **User Authentication**
  - Traditional username/password login
  - LINE social login integration
  - JWT-based authentication

- **Event Management**
  - Create, read, update, and delete events
  - Multi-language content support (English, Chinese)
  - Custom routing for different notification channels

- **Subscription System**
  - Users can subscribe/unsubscribe to events
  - View event subscribers
  - Track notification delivery status

- **Content Management**
  - Support for multiple languages per event (English, Chinese)
  - Dynamic content updating
  - Language-specific content delivery

- **Notification Channels**
  - Email notification support
  - LINE messaging integration (Not yet completed)

- **Activity Tracking**
  - Comprehensive event logging
  - User action recording
  - Notification delivery tracking

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT + OAuth2 (LINE integration)
- **Migration Tool**: Alembic
- **Dependency Management**: Poetry

## Setup Instructions

1. **Install Poetry**
   ```bash
   # Install dependencies using Poetry
   poetry install
   ```

2. **Database Setup**
   ```bash
   # Create database and run migrations
   alembic upgrade head
   ```

3. **Environment Variables**
   ```
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # LINE Integration
   LINE_CHANNEL_ID=your_line_channel_id
   LINE_CHANNEL_SECRET=your_line_channel_secret
   LINE_CALLBACK_URL=your_callback_url
   
   # Email Configuration
   GMAIL_SMTP_SERVER=smtp.gmail.com
   GMAIL_TLS_PORT=587
   GMAIL_SMTP_USERNAME=your_email
   GMAIL_SMTP_PASSWORD=your_app_password
   ```

4. **Running the Application**
   ```bash
   poetry run uvicorn command.server:app --reload --port 8000
   ```

## Project Structure

```
├── api
│   └── v1
│       ├── content.py      # Content management endpoints
│       ├── event.py        # Event management endpoints
│       ├── record.py       # Activity logging endpoints
│       ├── routes.py       # API route configuration
│       ├── trigger.py      # Notification trigger endpoints
│       └── user.py         # User management endpoints
├── database
│   ├── content.py          # Content model
│   ├── event.py           # Event model
│   ├── event_user.py      # Event subscription model
│   ├── record.py          # Activity log model
│   └── user.py            # User model
├── repository             # Database interaction layer
├── schema                 # Pydantic models
└── services              # Business logic layer
```

## Database Schema

### Core Tables
- **user**: User account information
- **event**: Event definitions and metadata
- **content**: Multi-language event content
- **event_user**: Event subscriptions
- **record**: System activity logs

## API Endpoints

### Authentication
- `POST /users/token`: Get JWT access token
- `GET /users/line-login`: Initiate LINE login
- `GET /users/callback`: LINE login callback

### Events
- `GET /events/`: List all events
- `POST /events/`: Create new event
- `PUT /events/{event_id}`: Update event
- `DELETE /events/{event_id}`: Delete event

### Content
- `GET /contents/{event_id}`: Get event content
- `POST /contents/{event_id}/{language}`: Add content
- `PUT /contents/{event_id}/{language}`: Update content
- `DELETE /contents/{event_id}/{language}`: Delete content

### Subscriptions
- `POST /events/{event_id}/subscribe`: Subscribe to event
- `DELETE /events/{event_id}/unsubscribe`: Unsubscribe from event
- `GET /events/{event_id}/subscribers`: List subscribers

### Triggers
- `GET /trigger/{event_id}/send_notification`: Trigger event notification
- `GET /trigger/{event_id}/notification_data`: Get notification data

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
