#!/usr/bin/python3

import cmd
from datetime import datetime
from shlex import shlex

from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
import models


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '
    clslist = {
        'BaseModel': BaseModel,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review,
        'User': User
    }

    def emptyline(self):
        """
        Do nothing when an empty line is entered.
        """
        pass

    def do_create(self, clsname=None):
        """
        Create a new instance of a given class.

        Args:
            clsname (str): The name of the class.

        Returns:
            None
        """
        if not clsname:
            print('** class name missing **')
        elif not self.clslist.get(clsname):
            print('** class doesn\'t exist **')
        else:
            obj = self.clslist[clsname]()
            models.storage.save()
            print(obj.id)

    def do_show(self, arg):
        """
        Display the string representation of an instance.

        Args:
            arg (str): The class name and instance id.

        Returns:
            None
        """
        clsname, objid = None, None
        args = arg.split(' ')
        if len(args) > 0:
            clsname = args[0]
        if len(args) > 1:
            objid = args[1]
        if not clsname:
            print('** class name missing **')
        elif not objid:
            print('** instance id missing **')
        elif not self.clslist.get(clsname):
            print("** class doesn't exist **")
        else:
            k = clsname + "." + objid
            obj = models.storage.all().get(k)
            if not obj:
                print('** no instance found **')
            else:
                print(obj)

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id.

        Args:
            arg (str): The class name and instance id.

        Returns:
            None
        """
        clsname, objid = None, None
        args = arg.split(' ')
        if len(args) > 0:
            clsname = args[0]
        if len(args) > 1:
            objid = args[1]
        if not clsname:
            print('** class name missing **')
        elif not objid:
            print('** instance id missing **')
        elif not self.clslist.get(clsname):
            print("** class doesn't exist **")
        else:
            k = clsname + "." + objid
            obj = models.storage.all().get(k)
            if not obj:
                print('** no instance found **')
            else:
                del models.storage.all()[k]
                models.storage.save()

    def do_all(self, arg):
        """
        Display all instances of a class or all instances.

        Args:
            arg (str): The class name (optional).

        Returns:
            None
        """
        if not arg:
            print([str(v) for k, v in models.storage.all().items()])
        else:
            if not self.clslist.get(arg):
                print("** class doesn't exist **")
                return False
            print([str(v) for k, v in models.storage.all().items()
                   if type(v) is self.clslist.get(arg)])

    def do_update(self, arg):
        """
        Update an instance attribute based on the class name and id.

        Args:
            arg (str): The class name, instance id, attribute name, and
            attribute value.

        Returns:
            None
        """
        clsname, objid, attrname, attrval = None, None, None, None
        updatetime = datetime.now()
        args = arg.split(' ', 3)
        if len(args) > 0:
            clsname = args[0]
        if len(args) > 1:
            objid = args[1]
        if len(args) > 2:
            attrname = args[2]
        if len(args) > 3:
            attrval = list(shlex(args[3]))[0].strip('"')
        if not clsname:
            print('** class name missing **')
        elif not objid:
            print('** instance id missing **')
        elif not attrname:
            print('** attribute name missing **')
        elif not attrval:
            print('** value missing **')
        elif not self.clslist.get(clsname):
            print("** class doesn't exist **")
        else:
            k = clsname + "." + objid
            obj = models.storage.all().get(k)
            if not obj:
                print('** no instance found **')
            else:
                if hasattr(obj, attrname):
                    attrval = type(getattr(obj, attrname))(attrval)
                else:
                    attrval = self.get_type(attrval)(attrval)
                setattr(obj, attrname, attrval)
                obj.updated_at = updatetime
                models.storage.save()

    def do_quit(self, arg):
        """
        Quit the command line interface.

        Args:
            arg (str): The argument passed (unused).

        Returns:
            True
        """
        return True

    def do_EOF(self, arg):
        """
        Quit the command line interface when the end-of-file character
        is reached.

        Args:
            arg (str): The argument passed (unused).

        Returns:
            True
        """
        return True

    def default(self, line):
        """
        Handle unknown commands.

        Args:
            line (str): The command entered.

        Returns:
            False
        """
        ln = line.split('.', 1)
        if len(ln) < 2:
            print('*** Unknown syntax:', ln[0])
            return False
        clsname, line = ln[0], ln[1]
        if clsname not in list(self.clslist.keys()):
            print('*** Unknown syntax: {}.{}'.format(clsname, line))
            return False
        ln = line.split('(', 1)
        if len(ln) < 2:
            print('*** Unknown syntax: {}.{}'.format(clsname, ln[0]))
            return False
        mthname, args = ln[0], ln[1].rstrip(')')
        if mthname not in ['all', 'count', 'show', 'destroy', 'update']:
            print('*** Unknown syntax: {}.{}'.format(clsname, line))
            return False
        if mthname == 'all':
            self.do_all(clsname)
        elif mthname == 'count':
            print(self.count_class(clsname))
        elif mthname == 'show':
            self.do_show(clsname + " " + args.strip('"'))
        elif mthname == 'destroy':
            self.do_destroy(clsname + " " + args.strip('"'))
        elif mthname == 'update':
            lb, rb = args.find('{'), args.find('}')
            d = None
            if args[lb:rb + 1] != '':
                d = eval(args[lb:rb + 1])
            ln = args.split(',', 1)
            objid, args = ln[0].strip('"'), ln[1]
            if d and type(d) is dict:
                self.handle_dict(clsname, objid, d)
            else:
                from shlex import shlex
                args = args.replace(',', ' ', 1)
                ln = list(shlex(args))
                ln[0] = ln[0].strip('"')
                self.do_update(" ".join([clsname, objid, ln[0], ln[1]]))

    def handle_dict(self, clsname, objid, d):
        """
        Handle updating attributes using a dictionary.

        Args:
            clsname (str): The class name.
            objid (str): The instance id.
            d (dict): The dictionary of attributes and values.

        Returns:
            None
        """
        for k, v in d.items():
            self.do_update(" ".join([clsname, objid, str(k), str(v)]))

    def postloop(self):
        """
        Print a newline after the command loop ends.

        Returns:
            None
        """
        print()

    @staticmethod
    def count_class(clsname):
        """
        Count the number of instances of a given class.

        Args:
            clsname (str): The class name.

        Returns:
            int: The number of instances.
        """
        c = 0
        for k, v in models.storage.all().items():
            if type(v).__name__ == clsname:
                c += 1
        return c

    @staticmethod
    def get_type(attrval):
        """
        Get the type of an attribute value.

        Args:
            attrval (str): The attribute value.

        Returns:
            type: The type of the attribute value.
        """
        try:
            int(attrval)
            return int
        except ValueError:
            pass
        try:
            float(attrval)
            return float
        except ValueError:
            return str


if __name__ == "__main__":
    HBNBCommand().cmdloop()
