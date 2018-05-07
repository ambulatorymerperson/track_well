@app.route('/my_stats')
def calculate_correlations():
    """Show user relationship between their behaviors and sense of wellness."""

    current_user = session['current_user']
    user_info = Daily_Input.query.filter_by(user_id=current_user).all()
