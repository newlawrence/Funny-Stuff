#include <sstream>

#include <cstdlib>
#include <cstdarg>
#include <cmath>
#include <cstring>

#include "semep.h"

namespace SEMEP {

	std::map<std::string, Expression::MemberConstant> Expression::constantList;
	std::map<std::string, Expression::MemberUnary> Expression::unaryList;
	std::map<std::string, Expression::MemberBinary> Expression::binaryList;
	Expression::MemberLeft Expression::leftObject;
	Expression::MemberRight Expression::rightObject;
	Expression::Initializer Expression::init;
	bool Expression::exceptions;

	Expression::Initializer::Initializer() {
		exceptions = true;
		Expression::addConstant("PI", 3.141592653589);
		Expression::addConstant("e", 2.718281828459);
		Expression::addUnary("neg", neg);
		Expression::addUnary("inv", inv);
		Expression::addUnary("exp", std::exp);
		Expression::addUnary("ln", std::log);
		Expression::addUnary("log", log_10);
		Expression::addUnary("sin", std::sin);
		Expression::addUnary("cos", std::cos);
		Expression::addUnary("tan", std::tan);
		Expression::addUnary("sinh", std::sinh);
		Expression::addUnary("cosh", std::cosh);
		Expression::addUnary("tanh", std::tanh);
		Expression::addUnary("asin", std::asin);
		Expression::addUnary("acos", std::acos);
		Expression::addUnary("atan", std::atan);
		Expression::addBinary("+", add, 30);
		Expression::addBinary("-", subs, 60);
		Expression::addBinary("*", prod, 90);
		Expression::addBinary("/", div, 120);
		Expression::addBinary("^", std::pow, 150);
	}

	const char* Expression::Error::what() const throw() {
		switch(error) {
        case(UNKNOWN):
            return "SEMEP Error: Unexpected error";
		case(EMPTY):
			return "SEMEP Error: Undefined expression";
		case(OUTRANGE):
			return "SEMEP Error: Access to no existent element";
		case(UNKNOWNMEMBER):
			return "SEMEP Error: Unexpected member in expression";
		case(OPERANDSTOGETHER):
			return "SEMEP Error: Operands side by side in expression";
		case(OPERATORSTOGETHER):
			return "SEMEP Error: Operators side by side in expression";
		case(BINARYFIRST):
			return "SEMEP Error: Binary operator first in expression";
		case(OPERATORLAST):
			return "SEMEP Error: Operator last in expression";
		case(BRACKETMISMATCH):
			return "SEMEP Error: Bracket mismatch";
		case(BRACKETSTOGETHER):
			return "SEMEP Error: Brackets together";
		case(OPERANDLEFT):
			return "SEMEP Error: Operand before left bracket";
		case(LEFTLAST):
			return "SEMEP Error: Left bracket last in expression";
		case(RIGHTFIRST):
			return "SEMEP Error: Right bracket first in expression";
		case(OPERATORRIGHT):
			return "SEMEP Error: Operator before right bracket";
		case(RIGHTOPERAND):
			return "SEMEP Error: Right bracket before operand";
		case(RIGHTOPERATOR):
			return "SEMEP Error: Right bracket before unary operator";
		}
		return "SEMEP Error: Unexpected error";
	}

	Expression::Expression() : varCount(0), builtFlag(false), errorFlag(false) {}

	Expression::Expression(const Expression &e) : varCount(0), builtFlag(false), errorFlag(false) {
		if(e.builtFlag)
			build(e.literal);
	}

	Expression::Expression(const std::string &s) : varCount(0), builtFlag(false), errorFlag(false) {
		build(s);
	}

	Expression::~Expression() {
		clear();
	}

	const Expression& Expression::operator=(const Expression &e) {
		if(e.builtFlag)
			build(e.literal);

        return *this;
	}

	const Expression& Expression::operator=(const std::string &s) {
		clear();
		build(s);

		return *this;
	}

	double Expression::operator()() {
		double x;

		try {
			if(!builtFlag) throw Error(EMPTY);

		}
		catch(Error &e) {
			errorFlag = true;
			if(exceptions) throw;
			lastError = e.what();
			return 0.0;
		}
		errorFlag = false;

		for(std::list<Member *>::iterator it = postfixList.begin(); it != postfixList.end(); ++it)
			(*it)->evaluate(outputStack);
		x = outputStack.top();
		outputStack.pop();
		return x;
	}

	double Expression::operator()(double x, ...) {
		double t;
		va_list pl;
		std::map<std::string, MemberVariable>::iterator vit;

		try {
			if(!builtFlag) throw Error(EMPTY);

		}
		catch(Error &e) {
			errorFlag = true;
			if(exceptions) throw;
			lastError = e.what();
			return 0.0;
		}
		errorFlag = false;

		va_start(pl, x);
		vit = variableList.begin();
		for(unsigned int i = 1; i <= varCount; i++) {
			vit->second.setValue(x);
			x = va_arg(pl, double);
			vit++;
		}
		va_end(pl);

		for(std::list<Member *>::iterator it = postfixList.begin(); it != postfixList.end(); ++it)
			(*it)->evaluate(outputStack);
		t = outputStack.top();
		outputStack.pop();

		return t;
	}

	void Expression::build(const std::string &s) {

		clear();
		literal = s;

		// Prepare the input string for detect objects

		{
			bool varmode = false;

			for(unsigned int i = 0; i < literal.size(); i++) {
				switch(literal[i]) {
				case(' '):
					break;
				case('('): case(')'): case('+'): case('-'):
				case('*'): case('/'): case('^'):
					internal += std::string(" ") += literal.substr(i, 1) += std::string(" ");
					break;
				case(','):
					varmode = true;
					break;
				default:
					internal += literal[i];
				}
				if(varmode) break;
			}
			if(varmode) {
				for(unsigned int i = literal.find(",", 0); i < literal.size(); i++) {
					switch(literal[i])
					{
					case(' '):
						break;
					case(','):
						internal += " _EXPRVar_ ";
						break;
					default:
						internal += literal[i];
					}
				}
			}
			internal += " _EXPRFinish_ _EXPRFinish_";
		}

		// Load variables

		{
			std::string object;
			std::istringstream stream;

			stream.str(internal);
			stream >> object;
			while(object != "_EXPRFinish_") {
				if(object == "_EXPRVar_") {
					stream >> object;
					if((object != "_EXPRVar_") && (object != "_EXPRFinish_"))
						addVariable(object);
					else
						break;
				}
				stream >> object;
			}
		}

		// Load infixList

		double t;

		try {
				{
					std::string object;
					std::istringstream stream;

					stream.str(internal);
					stream >> object;
					while((object != "_EXPRVar_") && (object != "_EXPRFinish_")) {
						t = strtod(object.c_str(), NULL);
						if(t) {
							addNumber(t);
							infixList.push_back(&numberList.back());
						}
						else {
							if(constantList.find(object) != constantList.end())
								infixList.push_back(&constantList.at(object));
							else if(variableList.find(object) != variableList.end())
								infixList.push_back(&variableList.at(object));
							else if(unaryList.find(object) != unaryList.end())
								infixList.push_back(&unaryList.at(object));
							else if(binaryList.find(object) != binaryList.end())
								infixList.push_back(&binaryList.at(object));
							else if(object == "(")
								infixList.push_back(&leftObject);
							else if(object == ")")
								infixList.push_back(&rightObject);
							else
								throw Error(UNKNOWNMEMBER);
						}
						stream >> object;
					}
				}

			// Check for sintax errors

			{
				std::list<Member *>::iterator it1, it2;
				unsigned int left, right;

				it1 = infixList.begin();
				it2 = infixList.begin();

				left = 0, right = 0;

				if((*it1)->getKind() == BinaryOperator) throw Error(BINARYFIRST);
				if((*it1)->getKind() == RightBracket) throw Error(RIGHTFIRST);

				if((*it1)->getKind() == LeftBracket) ++left;

				++it1;

				while(it1 != infixList.end()) {
					if(((*it2)->getGlobal() == Operand) && ((*it1)->getGlobal() == Operand))
						throw Error(OPERANDSTOGETHER);
					if(((*it2)->getKind() == UnaryOperator) && ((*it1)->getKind() == BinaryOperator))
						throw Error(OPERATORSTOGETHER);
					if(((*it2)->getKind() == BinaryOperator) && ((*it1)->getKind() == BinaryOperator))
						throw Error(OPERATORSTOGETHER);
					if(((*it2)->getGlobal() == Operand) && ((*it1)->getKind() == LeftBracket))
						throw Error(OPERANDLEFT);
					if(((*it2)->getKind() == LeftBracket) && ((*it1)->getKind() == RightBracket))
						throw Error(BRACKETSTOGETHER);
					if(((*it2)->getKind() == RightBracket) && ((*it1)->getKind() == LeftBracket))
						throw Error(BRACKETSTOGETHER);
					if(((*it2)->getKind() == RightBracket) && ((*it1)->getGlobal() == Operand))
						throw Error(RIGHTOPERAND);
					if(((*it2)->getGlobal() == Operator) && ((*it1)->getKind() == RightBracket))
						throw Error(OPERATORRIGHT);
					if(((*it2)->getKind() == RightBracket) && ((*it1)->getKind() == UnaryOperator))
						throw Error(RIGHTOPERATOR);

					if((*it1)->getKind() == LeftBracket) ++left;
					if((*it1)->getKind() == RightBracket) ++right;

                    ++it1;
					++it2;
				}
				if((*it2)->getGlobal() == Operator) throw Error(OPERATORLAST);
				if((*it2)->getKind() == LeftBracket) throw Error(LEFTLAST);
				if(left != right) throw Error(BRACKETMISMATCH);
			}

		}
		catch(Error &e) {
			clear();
			errorFlag = true;
			if(exceptions) throw;
			lastError = e.what();
			return;
		}

		// If everything OK, create postfixList from infixList

		for(std::list<Member *>::iterator it = infixList.begin(); it != infixList.end(); ++it) {
			switch((*it)->getKind()) {
			case(Number): case(Constant): case(Variable):
				postfixList.push_back(*it);
				break;
			case(UnaryOperator):
				operatorStack.push(*it);
				break;
			case(BinaryOperator):
				while((!operatorStack.empty()) && ((*it)->getPriority() <= operatorStack.top()->getPriority())) {
					if(operatorStack.top()->getKind() == LeftBracket)
						break;
					else {
						postfixList.push_back(operatorStack.top());
						operatorStack.pop();
					}
				}
				operatorStack.push(*it);
				break;
			case(LeftBracket):
				operatorStack.push(*it);
				break;
			case(RightBracket):
				while(!operatorStack.empty()) {
					if(operatorStack.top()->getKind() == LeftBracket) {
						operatorStack.pop();
						break;
					}
					else {
						postfixList.push_back(operatorStack.top());
						operatorStack.pop();
					}
				}
				break;
			}
		}
		while(!operatorStack.empty()) {
			postfixList.push_back(operatorStack.top());
			operatorStack.pop();
		}

		internal.clear(); // No more need of internal string
		infixList.clear(); // No more need of infixList;
		errorFlag = false;
		builtFlag = true; // Everything went OK
	}

	void Expression::clear() {
		literal.clear();
		internal.clear();

		varCount = 0;

		postfixList.clear();
		infixList.clear();
		while(!operatorStack.empty())
			operatorStack.pop();
		while(!outputStack.empty())
			outputStack.pop();

		numberList.clear();
		variableList.clear();

		errorFlag = false;
		builtFlag = false;
	}

	bool Expression::isBuilt() const {
		return builtFlag;
	}

	std::string Expression::getLiteral() const {
		std::string temp(literal);
		temp.resize(literal.find(",", 0));

		return temp;
	}

	std::string Expression::getVarName(unsigned int i) {
		std::map<std::string, MemberVariable>::iterator vit;

		vit = variableList.begin();
		try {
			if(i > varCount) throw Error(OUTRANGE);

			for(unsigned int j = 1; j < i; j++)
				vit++;
		}
		catch(Error &e) {
			errorFlag = true;
			if(exceptions) throw;
			lastError = e.what();
			return std::string("");
		}
		errorFlag = false;

		return vit->first;
	}

	unsigned int Expression::getVarCount() const {
		return varCount;
	}

	void Expression::throwExceptions(bool b) {
		exceptions = b;
	}
	
	bool Expression::checkError() {
		if(errorFlag) {
			errorFlag = false;
			return true;
		}
		return false;
	}

	std::string Expression::what() const {
		return lastError;
	}

	void Expression::addNumber(double x) {
		numberList.push_back(MemberNumber(x));
	}

	void Expression::addConstant(std::string s, double x) {
		if(constantList.find(s) == constantList.end())
			constantList.insert(std::make_pair(s, MemberConstant(x)));
	}

	void Expression::addVariable(std::string s) {
		if(variableList.find(s) == variableList.end()) {
			varCount++;
			variableList.insert(std::make_pair(s, MemberVariable(0.0)));
		}
	}

	void Expression::addUnary(std::string s, double (*f)(double x)) {
		if(unaryList.find(s) == unaryList.end())
			unaryList.insert(std::make_pair(s, MemberUnary(f)));
	}

	void Expression::addBinary(std::string s, double (*f)(double x, double y), unsigned char p) {
		if(binaryList.find(s) == binaryList.end())
			binaryList.insert(std::make_pair(s, MemberBinary(f, p)));
	}

	double neg(double x) {
		return -x;
	}

	double inv(double x) {
		return 1.0 / x;
	}

	double log_10(double x) {
		return std::log(x) / std::log(10.0);
	}

	double add(double x, double y) {
		return x + y;
	}

	double subs(double x, double y) {
		return x - y;
	}

	double prod(double x, double y) {
		return x * y;
	}

	double div(double x, double y) {
		return x / y;
	}

}

int SEMEP_create(SEMEP_Expression *e, const char *c) {
	SEMEP::Expression::throwExceptions(false);
	try {
		if(c)
			e->expression = new SEMEP::Expression(std::string(c));
		else
			e->expression = new SEMEP::Expression;
	}
	catch(std::bad_alloc) {
		return 1;
	}
	return 0;
}

void SEMEP_free(SEMEP_Expression *e) {
	delete e->expression;
}

double SEMEP_eval(SEMEP_Expression e, ...) {
	double r, s, t, u, v, w, x, y, z;
	va_list pl;

	va_start(pl, e);
	r = va_arg(pl, double);
	s = va_arg(pl, double);
	t = va_arg(pl, double);
	u = va_arg(pl, double);
	v = va_arg(pl, double);
	w = va_arg(pl, double);
	x = va_arg(pl, double);
	y = va_arg(pl, double);
	z = va_arg(pl, double);
	va_end(pl);

	return e.expression->operator()(r, s, t, u, v, w, x, y, z);
}

void SEMEP_build(SEMEP_Expression *e, const char *c) {
	e->expression->build(std::string(c));
}

void SEMEP_clear(SEMEP_Expression *e) {
	e->expression->clear();
}

int SEMEP_isBuilt(SEMEP_Expression e) {
	if(e.expression->isBuilt())
		return 1;
	return 0;	
}

void SEMEP_getLiteral(SEMEP_Expression e, char *c) {
	strcpy(c, e.expression->getLiteral().c_str());
}

void SEMEP_getVarName(SEMEP_Expression e, char *c, unsigned int i) {
	strcpy(c, e.expression->getVarName(i).c_str());
}

int SEMEP_getVarCount(SEMEP_Expression e) {
	return e.expression->getVarCount();
}

int SEMEP_checkError(SEMEP_Expression e) {
	if(e.expression->checkError())
		return 1;
	return 0;
}

void SEMEP_whatError(SEMEP_Expression e, char *c) {
	strcpy(c, e.expression->what().c_str());
}
