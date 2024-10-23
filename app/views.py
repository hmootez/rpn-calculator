from flask import jsonify, request
from flask import current_app


from app.constants import VALID_OPERATORS
from app.models import db, StackElement


# Route for pushing an element onto the stack
@current_app.route('/rpn/stack/push', methods=['POST'])
def push():
    """
    pop new element to the stack
    ---
    parameters:
      - name: value
        in: body
        type: string
        required: true
        description: value to push
    responses:
      200:
        description: element successfully pushed on the stack
      400:
        description: no given value
    """
    value = request.json.get('value')
    if value:
        new_element = StackElement(value=value)
        print(db.session)

        db.session.add(new_element)
        db.session.commit()
        return jsonify({'message': f'{value} pushed'}), 200
    else:
        return jsonify({'error': 'no given value'}), 400


# Route for popping an element from the stack
@current_app.route('/rpn/stack/pop', methods=['GET'])
def pop():
    """
    pop element from the stack
    ---
    responses:
      200:
        description: element popped successfully
      400:
        description: the stack is empty
    """
    last_element = StackElement.query.order_by(StackElement.id.desc()).first()
    if last_element:
        db.session.delete(last_element)
        db.session.commit()
        return jsonify({'message': f'{last_element.value} popped'}), 200
    else:
        return jsonify({'error': 'the stack is empty'}), 400


# Route for peeking the top element of the stack
@current_app.route('/rpn/stack/peek', methods=['GET'])
def peek():
    """
    get the top of the stack
    ---
    responses:
      200:
        description: top of the stack
      400:
        description: the stack is empty
    """
    last_element = StackElement.query.order_by(StackElement.id.desc()).first()
    if last_element:
        return jsonify({'message': f'Top: {last_element.value}'}), 200
    else:
        return jsonify({'error': 'the stack is empty'}), 400


# Route to clear the stack
@current_app.route('/rpn/stack', methods=['DELETE'])
def clear_stack():
    """
    delete all element in the stack
    ---
    responses:
      200:
        description: all elements are deleted
    """
    try:
        # Delete all records from the StackElement table
        db.session.query(StackElement).delete()
        db.session.commit()
        return jsonify({'message': 'all elements are deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': e}), 500


# Route for peeking the top element of the stack
@current_app.route('/rpn/op', methods=['GET'])
def get_operands():
    """
    List all the operands
    ---
    responses:
      200:
        description: all the operands
    """

    return jsonify({'message': '+, -, *, /'}), 200


# Route for apply operation to stack
@current_app.route('/rpn/apply', methods=['POST'])
def apply():
    """
    apply operator to the stack
    ---
    parameters:
      - name: operator
        in: body
        type: string
        required: true
        description: value to push
    responses:
      200:
        description: operator applied successfully to the stack
      400:
        description: no given valid operator value
    """
    operator = request.json.get('operator')

    if operator not in VALID_OPERATORS:
        return jsonify({'error': 'not valid operator'}), 400
    elements = StackElement.query.order_by(StackElement.id.desc()).limit(2).all()
    if len(elements) < 2:
        return jsonify({'message': 'operands are not found'}), 500

    last_element, second_last_element = elements
    # Define operations in a dictionary
    operations = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
    }

    try:
        result = operations[operator](last_element.value, second_last_element.value)

        # Delete the concerned values from the StackElement table
        db.session.delete(last_element)
        db.session.delete(second_last_element)
        new_element = StackElement(value=result)
        db.session.add(new_element)
        db.session.commit()
        return jsonify({'message': 'concerned values are deleted and result is pushed'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

