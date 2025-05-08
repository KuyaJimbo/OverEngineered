# Complete Guide to UML Class Diagram Relationships and Symbols

## Table of Contents
- [Complete Guide to UML Class Diagram Relationships and Symbols](#complete-guide-to-uml-class-diagram-relationships-and-symbols)
  - [Table of Contents](#table-of-contents)
  - [Introduction to UML Class Diagrams ](#introduction-to-uml-class-diagrams-)
  - [Class Notation ](#class-notation-)
  - [Attributes and Operations ](#attributes-and-operations-)
    - [Attributes Syntax:](#attributes-syntax)
    - [Operations Syntax:](#operations-syntax)
  - [Visibility Modifiers ](#visibility-modifiers-)
  - [Relationships Between Classes ](#relationships-between-classes-)
    - [Association ](#association-)
    - [Aggregation ](#aggregation-)
    - [Composition ](#composition-)
    - [Inheritance/Generalization ](#inheritancegeneralization-)
    - [Realization/Implementation ](#realizationimplementation-)
    - [Dependency ](#dependency-)
  - [Multiplicity ](#multiplicity-)
  - [Advanced Concepts ](#advanced-concepts-)
    - [Abstract Classes ](#abstract-classes-)
    - [Interfaces ](#interfaces-)
    - [Static Members ](#static-members-)
    - [Enumeration ](#enumeration-)
    - [Constraints ](#constraints-)
  - [Best Practices ](#best-practices-)
  - [Example Diagram ](#example-diagram-)

## Introduction to UML Class Diagrams <a name="introduction"></a>

UML (Unified Modeling Language) class diagrams are used to visualize the structure of a system by showing:
- Classes with their attributes and operations
- Relationships between classes
- Inheritance hierarchies
- Associations and dependencies

Class diagrams are essential in object-oriented design and are used during various phases of software development to:
- Design new systems
- Document existing systems
- Communicate system architecture
- Generate code or database schemas

## Class Notation <a name="class-notation"></a>

A class is represented by a rectangle divided into three compartments:

```
┌───────────────────┐
│     ClassName     │ ← Class name (first compartment)
├───────────────────┤
│   + attribute1    │
│   - attribute2    │ ← Attributes (second compartment)
│   # attribute3    │
├───────────────────┤
│   + operation1()  │
│   - operation2()  │ ← Operations/Methods (third compartment)
│   # operation3()  │
└───────────────────┘
```

- The top compartment contains the class name (bold and centered)
- The middle compartment contains attributes (properties or fields)
- The bottom compartment contains operations (methods or functions)

## Attributes and Operations <a name="attributes-and-operations"></a>

### Attributes Syntax:
```
visibility name: type [multiplicity] = defaultValue {property-string}
```

Examples:
- `- name: String`
- `+ age: Integer = 0`
- `# addresses: Address[0..*]`

### Operations Syntax:
```
visibility name(parameter-list): return-type {property-string}
```

Examples:
- `+ getName(): String`
- `- calculateSalary(hours: Integer): Double`
- `# updateAddress(address: Address): void`

## Visibility Modifiers <a name="visibility-modifiers"></a>

UML defines the following visibility modifiers:

| Symbol | Visibility | Meaning                                        |
| ------ | ---------- | ---------------------------------------------- |
| `+`    | Public     | Accessible to all classes                      |
| `-`    | Private    | Accessible only within the class               |
| `#`    | Protected  | Accessible within the class and its subclasses |
| `~`    | Package    | Accessible within the same package (namespace) |

## Relationships Between Classes <a name="relationships"></a>

### Association <a name="association"></a>

An association represents a relationship between two classes where both classes are aware of each other and communicate with each other.

**Symbol:** Solid line connecting two classes

```
┌─────────┐             ┌─────────┐
│ Class A │─────────────│ Class B │
└─────────┘             └─────────┘
```

**Directional Association:** Arrow pointing to the known class

```
┌─────────┐             ┌─────────┐
│ Class A │──────────-->│ Class B │
└─────────┘             └─────────┘
```

Indicates Class A knows about Class B, but Class B doesn't know about Class A.

### Aggregation <a name="aggregation"></a>

Aggregation represents a "whole-part" relationship where one class (the whole) contains references to other classes (the parts). The parts can exist independently of the whole.

**Symbol:** Empty diamond on the "whole" side and a solid line to the "part" side

```
┌─────────┐        ◇───────┌─────────┐
│ Student │────────────────│ Course  │
└─────────┘                └─────────┘
  (Part)                     (Whole)
```

In this example, a Course contains Students, but Students can exist independently of a specific Course.

### Composition <a name="composition"></a>

Composition is a stronger form of aggregation where the "part" cannot exist without the "whole." If the "whole" is destroyed, all its "parts" are destroyed as well.

**Symbol:** Filled diamond on the "whole" side and a solid line to the "part" side

```
┌─────────┐        ♦───────┌─────────┐
│  Room   │────────────────│  House  │
└─────────┘                └─────────┘
  (Part)                     (Whole)
```

In this example, a Room cannot exist outside of a House. If the House is demolished, its Rooms cease to exist.

### Inheritance/Generalization <a name="inheritance"></a>

Inheritance represents an "is-a" relationship where a subclass inherits attributes and operations from a superclass.

**Symbol:** Empty triangle pointing to the superclass (parent) with a solid line connecting to the subclass (child)

```
      ┌───────────┐
      │  Animal   │
      └─────▲─────┘
            │
            │
  ┌─────────┴─────────┐
  │                   │
┌─┴───────┐     ┌─────┴───┐
│   Dog   │     │   Cat   │
└─────────┘     └─────────┘
```

In this example, Dog and Cat are subclasses of Animal, inheriting Animal's attributes and operations.

### Realization/Implementation <a name="realization"></a>

Realization represents a relationship where one class implements an interface (or an abstract class).

**Symbol:** Empty triangle pointing to the interface with a dashed line connecting to the implementing class

```
      ┌───────────┐
      │«interface»│
      │ Printable │
      └─────▲─────┘
            :
            :
┌───────────┴───────────┐
│         Report        │
└───────────────────────┘
```

In this example, Report implements the Printable interface.

### Dependency <a name="dependency"></a>

Dependency represents a relationship where one class uses another class, typically as a method parameter, local variable, or return type.

**Symbol:** Dashed line with an arrow pointing to the class being used (depended upon)

```
┌─────────┐             ┌─────────┐
│ Class A │- - - - - - >│ Class B │
└─────────┘             └─────────┘
```

In this example, Class A depends on Class B (e.g., Class A uses Class B as a parameter in one of its methods).

## Multiplicity <a name="multiplicity"></a>

Multiplicity indicates how many objects participate in a relationship. It is shown near the ends of an association.

Common multiplicity indicators:

| Notation        | Meaning                  |
| --------------- | ------------------------ |
| `1`             | Exactly one              |
| `*` (or `0..*`) | Zero or more             |
| `0..1`          | Zero or one (optional)   |
| `1..*`          | One or more              |
| `m..n`          | At least m and at most n |

Example:

```
┌─────────┐ 1      0..* ┌─────────┐
│ Teacher │───────────◆│ Student │
└─────────┘             └─────────┘
```

This indicates that one Teacher can have many (zero or more) Students, and each Student belongs to exactly one Teacher.

## Advanced Concepts <a name="advanced-concepts"></a>

### Abstract Classes <a name="abstract-classes"></a>

Abstract classes cannot be instantiated and are often used as base classes.

**Notation:** Class name is in italics or has `{abstract}` property

```
┌───────────────┐
│ *AbstractClass* │
└───────────────┘
```

or

```
┌───────────────┐
│ AbstractClass │
│  {abstract}   │
└───────────────┘
```

### Interfaces <a name="interfaces"></a>

Interfaces define a contract without implementation.

**Notation:** Class rectangle with «interface» stereotype above the name or a circle (lollipop) notation

```
┌───────────────┐
│  «interface»  │
│   Printable   │
└───────────────┘
```

or with lollipop notation:

```
      ┌─────────┐
      │ Class A │
      └────┬────┘
           │
         ◯───── «interface» Printable
```

### Static Members <a name="static-members"></a>

Static (class-level) attributes and operations are underlined in UML.

```
┌───────────┐
│  ClassName│
├───────────┤
│+ attribute│
├───────────┤
│+ operation()│
└───────────┘
```

### Enumeration <a name="enumeration"></a>

An enumeration is a data type with predefined values.

```
┌──────────────┐
│ «enumeration»│
│    Season    │
├──────────────┤
│   SPRING     │
│   SUMMER     │
│   AUTUMN     │
│   WINTER     │
└──────────────┘
```

### Constraints <a name="constraints"></a>

Constraints are specified in curly braces `{}` and can be attached to any UML element.

```
┌────────────┐        ┌────────────┐
│   Person   │────────│   Address  │
└────────────┘{unique}└────────────┘
```

## Best Practices <a name="best-practices"></a>

1. **Keep it simple**: Include only relevant classes and relationships.
2. **Use consistent naming**: Follow naming conventions for classes, attributes, and operations.
3. **Group related classes**: Position related classes near each other.
4. **Add notes where necessary**: Use note elements to clarify complex parts.
5. **Avoid crossing lines**: Arrange classes to minimize line crossings.
6. **Show only necessary details**: Hide attributes and operations when focusing on relationships.
7. **Use packages**: Group related classes into packages for large diagrams.
8. **Include directionality**: Show direction of relationships when relevant.

## Example Diagram <a name="example-diagram"></a>

Here's a comprehensive example of a UML class diagram for a simple library management system:

```
┌───────────────────────┐         ┌────────────────────┐
│        Person         │         │      Address       │
├───────────────────────┤         ├────────────────────┤
│- name: String         │1       1│- street: String    │
│- id: String {unique}  │─────────│- city: String      │
│- phone: String[0..3]  │         │- state: String     │
├───────────────────────┤         │- zipCode: String   │
│+ getName(): String    │         └────────────────────┘
│+ setName(n: String)   │
└─────────┬─────────────┘
          │ 
          │ {complete, disjoint}
          │
┌─────────┴───────────┐           ┌────────────────────┐
│       Member        │           │      Library       │
├─────────────────────┤           ├────────────────────┤
│- memberId: String   │0..*     1 │- name: String      │
│- joinDate: Date     │◆─────────│- location: Address │
├─────────────────────┤           ├────────────────────┤
│+ checkoutBook()     │           │+ addBook()         │
│+ returnBook()       │           │+ removeBook()      │
└─────────┬───────────┘           ┴────────────────────┘
          │                   owns│
┌─────────┴───────────┐         ┌─┴────────────────────┐
│    Librarian        │manages  │         Book         │
├─────────────────────┤- - - - -├───────────────────── │
│- staffId: String    │         │- isbn: String        │
│- hireDate: Date     │         │- title: String       │
├─────────────────────┤         │- author: String      │
│+ addMember()        │1      * ┴───────────────────── │
│+ removeMember()     │         │+ getAvailability()   │
└─────────────────────┘         └─────────────────────┘
```

This diagram shows:
- Inheritance: Person is the parent class of Member and Librarian
- Association: Member can check out Books from the Library
- Composition: Library owns Books (filled diamond)
- Aggregation: Library has an Address (empty diamond)
- Dependency: Librarian manages Books (dashed line)
- Multiplicity: One Library can have many Books (1 to *)

Remember that UML diagrams should be tailored to their specific purpose and audience. Include only what's necessary to communicate the intended information effectively.