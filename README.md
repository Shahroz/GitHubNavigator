# GitHubNavigator
A Sample Django search repository app using Github API v3 and uWSGI for assignment purpose.

Make Sure you have Linux/OSX Environment

Follows Django best practices as much as possible. 

Installation steps on Debian 8
------------------------------

- Install uWSGI as system-wide services.

    ```
    apt-get install uwsgi
    ```

Installation steps on OSX
------------------------------

- Install uWSGI as system-wide services.

    ```
    brew install uwsgi
    ```
------------------------------
- `git clone` this repo into any directroy.

    ```
    cd /path/to/your/directory/
    git clone https://github.com/Shahroz/GitHubNavigator.git
    ```

- Create a virtualenv with the latest `pip`, `setuptools`, and `django` packages.
    ```
    cd /path/to/your/directory/GitHubNavigator
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    ```
- Finally Serve Django Project with uWSGI.

    ```
    uwsgi --socket /path/to/your/directory/GitHubNavigator/GitHubNavigator.sock --http :8000 --module GitHubNavigator.wsgi:application --enable-threads --home env --vacuum --master
    ```
- Check it out!

    ```
    http://localhost:8000/GitHubNavigator/navigator?search_term="<search here for repository>"
    ```
