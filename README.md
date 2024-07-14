# macostudios

macostudios is an intelligent movie and series recommendation app that leverages AI to display users' favorite movies and series based on their choices. The app is built primarily with Django and utilizes a PostgreSQL database.

## Features

- **AI-Powered Recommendations**: Uses AI algorithms to recommend movies and series tailored to each user’s preferences.
- **User-Friendly Interface**: Intuitive design for seamless navigation and interaction.
- **Personalized Profiles**: Each user has a personalized profile page showcasing their favorite movies and series.
- **Extensive Database**: Utilizes a robust PostgreSQL database to manage and store user data and movie/series information.

## Technologies Used

- **Backend**: Django
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **AI Algorithms**: Python (specific libraries and models used can be listed here if applicable)

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.8+
- Django 3.2+
- PostgreSQL 12+

### Installation

1. **Clone the repository:**

    git clone https://github.com/Lawrence496/macostudios.git
    cd macostudios

2. **Create a virtual environment and activate it:**

    python -m venv venv
    source venv/bin/activate

3. **Install the required packages:**

    pip install -r requirements.txt

4. **Configure the PostgreSQL database:**

   Update the `DATABASES` settings in `macostudios/settings.py` to match your PostgreSQL configuration.

  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'your_db_name',
          'USER': 'your_db_user',
          'PASSWORD': 'your_db_password',
          'HOST': 'your_db_host',
          'PORT': 'your_db_port',
      }
  }

5. **Apply migrations:**

    python manage.py migrate

6. **Run the development server:**

    python manage.py runserver


    Open your browser and navigate to `http://127.0.0.1:8000` to see the app in action.

## Usage

1. **Sign Up/Login**: Create an account or log in to your existing account.
2. **Set Preferences**: Choose your favorite genres.
3. **Get Recommendations**: View personalized movie and series recommendations on your profile page.
4. **Explore**: Browse through the extensive collection of movies and series.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by various AI and movie recommendation projects.

---
