from streamlit.web import cli
# from streamlit.runtime.scriptrunner import magic_funcs

if __name__ == '__main__':
    cli._main_run_clExplicit('app.py', 'streamlit run')
