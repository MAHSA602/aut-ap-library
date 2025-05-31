from flask import Flask, request, jsonify

app = Flask(__name__)

#  list to store projects
projects = []

# get all projects
@app.route('/projects', methods=['GET'])
def get_projects():
    return jsonify(projects), 200

# get a project by id
@app.route('/projects/<int:id>', methods=['GET'])
def get_project(id):
    for project in projects:
        if project['id'] == id:
            return jsonify(project), 200
    return jsonify({'error': 'project not found'}), 404

# add a new project
@app.route('/projects', methods=['POST'])
def create_project():
    if not request.is_json:
        return jsonify({'error': 'request must be json'}), 400
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'name is required'}), 400
    new_project = {
        'id': len(projects) + 1,
        'name': data['name']
    }
    projects.append(new_project)
    return jsonify(new_project), 201

# delete a project by id
@app.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    global projects
    for i, project in enumerate(projects):
        if project['id'] == id:
            projects.pop(i)
            return jsonify({'message': 'project deleted'}), 200
    return jsonify({'error': 'project not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)