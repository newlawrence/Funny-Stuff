#ifndef _SEMEP_HPP_
#define _SEMEP_HPP_

#ifdef __cplusplus
	
	#include <string>
	#include <list>
	#include <stack>
	#include <map>
	
	namespace SEMEP {
		
		class Expression {
			
		private:
			
			enum MemberGlobal {Operand, Operator, Bracket};
			
			enum MemberKind {Number, Constant, Variable, UnaryOperator, BinaryOperator, LeftBracket, RightBracket};
			
			class Member {
			private:
				MemberGlobal global;
				MemberKind kind;
				unsigned char priority;
			public:
				Member(MemberKind k, MemberGlobal g, unsigned char p) : global(g), kind(k), priority(p) {}
				virtual ~Member() {}
				virtual void evaluate(std::stack<double> &s) const = 0;
				MemberGlobal getGlobal() const {return global;}
				MemberKind getKind() const {return kind;}
				unsigned char getPriority() const {return priority;}
			};
			
			class MemberOperand : public Member {
			protected:
				double value;
			public:
				MemberOperand(MemberKind k, double d) : Member(k, Operand, 0), value(d) {}
				virtual ~MemberOperand() {}
				virtual void evaluate(std::stack<double> &s) const = 0;
			};
			
			class MemberOperator : public Member {
			public:
				MemberOperator(MemberKind k, unsigned char p) : Member(k, Operator, p) {}
				virtual ~MemberOperator() {}
				virtual void evaluate(std::stack<double> &s) const = 0;
			};
			
			class MemberBracket : public Member {
			public:
				MemberBracket(MemberKind k) : Member(k, Bracket, 255) {}
				virtual ~MemberBracket() {}
				virtual void evaluate(std::stack<double> &s) const = 0;
			};
			
			class MemberNumber : public MemberOperand {
			public:
				MemberNumber(double d) : MemberOperand(Number, d) {}
				~MemberNumber() {}
				void evaluate(std::stack<double> &s) const {s.push(value);}
			};
			
			class MemberConstant : public MemberOperand {
			public:
				MemberConstant(double d) : MemberOperand(Constant, d) {}
				~MemberConstant() {}
				void evaluate(std::stack<double> &s) const {s.push(value);}
			};
			
			class MemberVariable : public MemberOperand {
			public:
				MemberVariable(double d) : MemberOperand(Variable, d) {}
				~MemberVariable() {}
				void evaluate(std::stack<double> &s) const {s.push(value);}
				void setValue(double x) {value = x;}
			};
			
			class MemberUnary : public MemberOperator {
			protected:
				double (*function)(double x);
			public:
				MemberUnary(double (*f)(double x)) : MemberOperator(UnaryOperator, 254), function(f) {}
				~MemberUnary() {}
				void evaluate(std::stack<double> &s) const {
					double x;
					x = s.top();
					s.pop();
					s.push(function(x));
				}
			};
			
			class MemberBinary : public MemberOperator {
			protected:
				double (*function)(double x, double y);
			public:
				MemberBinary(double (*f)(double x, double y), unsigned char p) : MemberOperator(BinaryOperator, p), function(f) {}
				~MemberBinary() {}
				void evaluate(std::stack<double> &s) const {
					double x, y;
					y = s.top();
					s.pop();
					x = s.top();
					s.pop();
					s.push(function(x, y));
				}
			};
			
			class MemberLeft : public MemberBracket {
			public:
				MemberLeft() : MemberBracket(LeftBracket) {}
				~MemberLeft() {}
				void evaluate(std::stack<double> &s) const {}
			};
			
			class MemberRight : public MemberBracket {
			public:
				MemberRight() : MemberBracket(RightBracket) {}
				~MemberRight() {}
				void evaluate(std::stack<double> &s) const {}
			};
			
			class Initializer {
			public:
				Initializer();
			};
			
			friend class Initializer;
			
			enum ErrorKind {UNKNOWN, EMPTY, OUTRANGE, UNKNOWNMEMBER, OPERANDSTOGETHER,
				OPERATORSTOGETHER, BINARYFIRST, OPERATORLAST, BRACKETMISMATCH, BRACKETSTOGETHER,
				OPERANDLEFT, LEFTLAST, RIGHTFIRST, RIGHTOPERAND, OPERATORRIGHT, RIGHTOPERATOR};
			
			class Error : public std::exception {
			private:
				ErrorKind error;
			public:
				Error() : error(UNKNOWN) {}
				Error(ErrorKind e) : error(e) {}
				const char* what() const throw();
			};
			
			static Initializer init;
			
			std::list<MemberNumber> numberList;
			static std::map<std::string, MemberConstant> constantList;
			std::map<std::string, MemberVariable> variableList;
			static std::map<std::string, MemberUnary> unaryList;
			static std::map<std::string, MemberBinary> binaryList;
			static MemberLeft leftObject;
			static MemberRight rightObject;
			
			std::string literal;
			std::string internal;
			
			unsigned int varCount;
			
			bool builtFlag;
			bool errorFlag;
			static bool exceptions;
			std::string lastError;
			
			std::list<Member *> postfixList;
			std::list<Member *> infixList;
			std::stack<Member *> operatorStack;
			std::stack<double> outputStack;
			
		public:
			Expression();
			Expression(const Expression &e);
			Expression(const std::string &s);
			~Expression();
			const Expression& operator=(const Expression &e);
			const Expression& operator=(const std::string &s);
			double operator()();
			double operator()(double x, ...);
			
			void build(const std::string &s);
			void clear();
			bool isBuilt() const;
			
			std::string getLiteral() const;
			std::string getVarName(unsigned int i);
			unsigned int getVarCount() const;
			
			static void throwExceptions(bool b);
			bool checkError();
			std::string what() const;
			
		private:
			void addNumber(double x);
			void addVariable(std::string s);
			
		public:
			static void addConstant(std::string s, double x);
			static void addUnary(std::string s, double (*f)(double x));
			
		private:
			static void addBinary(std::string s, double (*f)(double x, double y), unsigned char p);
		};
		
		double neg(double x);
		
		double inv(double x);
		
		double log_10(double x);
		
		double add(double x, double y);
		
		double subs(double x, double y);
		
		double prod(double x, double y);
		
		double div(double x, double y);
		
	}
	
	struct SEMEP_Expression_t {
	SEMEP::Expression *expression;
	};
	typedef SEMEP_Expression_t SEMEP_Expression;
	
#else
	
	struct SEMEP_Expression_t {
	void *expression;
	};
	typedef struct SEMEP_Expression_t SEMEP_Expression;
	
#endif

#ifdef __cplusplus
	extern "C" {
#endif

int SEMEP_create(SEMEP_Expression *e, const char *c);
void SEMEP_free(SEMEP_Expression *e);

double SEMEP_eval(SEMEP_Expression e, ...);

void SEMEP_build(SEMEP_Expression *e, const char *c);
void SEMEP_clear(SEMEP_Expression *e);
int SEMEP_isBuilt(SEMEP_Expression e);

void SEMEP_getLiteral(SEMEP_Expression e, char *c);
void SEMEP_getVarName(SEMEP_Expression e, char *c, unsigned int i);
int SEMEP_getVarCount(SEMEP_Expression e);

int SEMEP_checkError(SEMEP_Expression e);
void SEMEP_whatError(SEMEP_Expression e, char *c);

#ifdef __cplusplus
	}
#endif

#endif
