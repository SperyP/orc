import os
from flask import Flask, render_template
from datetime import timedelta
from .popular_repos import get_popular_repos
# app = Flask(__name__, template_folder='../templates/orc_site')
app = Flask(__name__)


context = {
    'version': 'beta',
    'test_version': 'test-beta',
    'home_url': '/',
    'jhub_url': '/jupyter/',
    'gesis_login_url': 'https://notebooks{}.gesis.org/Shibboleth.sso/Login?SAMLDS=1&'
                       'target=https://notebooks{}.gesis.org/jupyter/hub/login&'
                       'entityID=https%3A%2F%2Fidp.gesis.org%2Fidp%2Fshibboleth'.
                       format(*['-test', '-test'] if os.environ.get('DEPLOYMENT_ENV') == 'staging' else ['', '']),
    'bhub_url': '/binder/',
    'about_url': '/about/',
    'tou_url': '/terms_of_use/',
    'imprint_url': 'https://www.gesis.org/en/institute/imprint/',
    'data_protection_url': 'https://www.gesis.org/en/institute/data-protection/',
    'contact_url': 'mailto:notebooks@gesis.org',
    'gesis_url': 'https://www.gesis.org/en/home/',
    'help_url': 'https://www.gesis.org/en/help/',
    'shibboleth_entityID': 'https://notebooks.gesis.org/shibboleth',
    'test_shibboleth_entityID': 'https://notebooks-test.gesis.org/shibboleth',
    'is_staging': os.environ.get('DEPLOYMENT_ENV') == 'staging',
    'is_production': os.environ.get('DEPLOYMENT_ENV') == 'production'
}


@app.errorhandler(404)
def not_found(error):
    context.update({'status_code': error.code,
                    'status_message': error.name,
                    'message': error.description,
                    'active': None})
    return render_template('error.html', **context), 404


@app.route('/')
def home():
    domain = 'https://notebooks{}.gesis.org'.format('-test' if os.environ.get('DEPLOYMENT_ENV') == 'staging' else '')
    binder_examples = [
        {'headline': 'Girls Day Hackathon',
         'content': '',
         'binder_link': '{}/binder/v2/gh/gesiscss/workshop_girls_day/master'.format(domain),
         'repo_link': 'https://github.com/gesiscss/workshop_girls_day'},
        {'headline': 'Python Data Science Handbook',
         'content': '',
         'binder_link': '{}/binder/v2/gh/gesiscss/PythonDataScienceHandbook/master'.format(domain),
         'repo_link': 'https://github.com/gesiscss/PythonDataScienceHandbook'},
        {'headline': 'LIGO Binder',
         'content': '',
         'binder_link': '{}/binder/v2/gh/minrk/ligo-binder/master'.format(domain),
         'repo_link': 'https://github.com/minrk/ligo-binder'},
    ]
    context.update({'active': 'home', 'binder_examples': binder_examples})
    return render_template('home.html', **context)


@app.route('/login/')
def login():
    context.update({'active': 'login'})
    return render_template('shibboleth_login.html', **context)


@app.route('/about/')
def about():
    context.update({'active': 'about'})
    return render_template('about.html', **context)


@app.route('/terms_of_use/')
def terms_of_use():
    context.update({'active': 'terms_of_use'})
    return render_template('terms_of_use.html', **context)


@app.route('/gallery/')
def gallery():
    popular_repos_1d = get_popular_repos('1d', timedelta(days=1))
    context.update({'active': 'test',
                    'popular_repos_1h': get_popular_repos('1h', timedelta(hours=1)),
                    'popular_repos_1d': get_popular_repos('1d', timedelta(days=1)),
                    'popular_repos_1w': get_popular_repos('7d', timedelta(days=7)),
                    'popular_repos_1m': get_popular_repos('30d', timedelta(days=30)),
                    'popular_repos_all': get_popular_repos('60d', timedelta(days=60)),
                    })
    return render_template('gallery.html', **context)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
