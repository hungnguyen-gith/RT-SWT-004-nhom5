def process_nested_expression(self, nested_expression) -> str:
        """
        ``nested_expression`` is the result of parsing a logical form in Lisp format.
        We process it recursively and return a string in the format that NLTK's ``LogicParser``
        would understand.
        """
        expression_is_list = isinstance(nested_expression, list)
        expression_size = len(nested_expression)
        if expression_is_list and expression_size == 1 and isinstance(nested_expression[0], list):
            return self.process_nested_expression(nested_expression[0])
        elements_are_leaves = [isinstance(element, str) for element in nested_expression]
        if all(elements_are_leaves):
            mapped_names = [self._map_name(name) for name in nested_expression]
        else:
            mapped_names = []
            for element, is_leaf in zip(nested_expression, elements_are_leaves):
                if is_leaf:
                    mapped_names.append(self._map_name(element))
                else:
                    mapped_names.append(self.process_nested_expression(element))
        if mapped_names[0] == "\\":
            # This means the predicate is lambda. NLTK wants the variable name to not be within parantheses.
            # Adding parentheses after the variable.
            arguments = [mapped_names[1]] + [f"({name})" for name in mapped_names[2:]]
        else:
            arguments = [f"({name})" for name in mapped_names[1:]]
        return f'({mapped_names[0]} {" ".join(arguments)})'