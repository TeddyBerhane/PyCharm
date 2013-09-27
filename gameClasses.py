# XML Parser/Data Access Object game.xml.py
"""AUTO-GENERATED Source file for game.xml.py"""
import xml.sax
import Queue
import Q2API.xml.base_xml

rewrite_name_list = ("name", "value", "attrs", "flatten_self", "flatten_self_safe_sql_attrs", "flatten_self_to_utf8", "children")

def process_attrs(attrs):
    """Process sax attribute data into local class namespaces"""
    if attrs.getLength() == 0:
        return {}
    tmp_dict = {}
    for name in attrs.getNames():
        tmp_dict[name] = attrs.getValue(name)
    return tmp_dict

def clean_node_name(node_name):
    clean_name = node_name.replace(":", "_").replace("-", "_").replace(".", "_")

    if clean_name in rewrite_name_list:
        clean_name = "_" + clean_name + "_"

    return clean_name

class Ammo_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'Building', u'Room', u'Items']
        Q2API.xml.base_xml.XMLNode.__init__(self, "Ammo", attrs, None, [])

class BattleMusic_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'Building', u'Room', u'Monster']
        Q2API.xml.base_xml.XMLNode.__init__(self, "BattleMusic", attrs, None, [])

class ItemArt_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'Building', u'Room', u'Items']
        Q2API.xml.base_xml.XMLNode.__init__(self, "ItemArt", attrs, None, [])

class ItemDes_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'Building', u'Room', u'Items']
        Q2API.xml.base_xml.XMLNode.__init__(self, "ItemDes", attrs, None, [])

class ItemSound_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'Building', u'Room', u'Items']
        Q2API.xml.base_xml.XMLNode.__init__(self, "ItemSound", attrs, None, [])

class ItemUse_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'Building', u'Room', u'Items']
        Q2API.xml.base_xml.XMLNode.__init__(self, "ItemUse", attrs, None, [])

class MonsterArt_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'Building', u'Room', u'Monster']
        Q2API.xml.base_xml.XMLNode.__init__(self, "MonsterArt", attrs, None, [])

class MonsterAttack_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'Building', u'Room', u'Monster']
        Q2API.xml.base_xml.XMLNode.__init__(self, "MonsterAttack", attrs, None, [])

class MonsterDes_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'Building', u'Room', u'Monster']
        Q2API.xml.base_xml.XMLNode.__init__(self, "MonsterDes", attrs, None, [])

class ReqMes_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'Building', u'Room', u'Req']
        Q2API.xml.base_xml.XMLNode.__init__(self, "ReqMes", attrs, None, [])

class ReqSound_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'Building', u'Room', u'Req']
        Q2API.xml.base_xml.XMLNode.__init__(self, "ReqSound", attrs, None, [])

class UseSound_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'Building', u'Room', u'Items']
        Q2API.xml.base_xml.XMLNode.__init__(self, "UseSound", attrs, None, [])

class Art_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'Building', u'Room']
        Q2API.xml.base_xml.XMLNode.__init__(self, "Art", attrs, None, [])

class Des_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'Building', u'Room']
        Q2API.xml.base_xml.XMLNode.__init__(self, "Des", attrs, None, [])

class Event_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'Building', u'Room']
        Q2API.xml.base_xml.XMLNode.__init__(self, "Event", attrs, None, [])

class Exit_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'Building', u'Room']
        Q2API.xml.base_xml.XMLNode.__init__(self, "Exit", attrs, None, [])

class Items_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'Building', u'Room']
        self.ItemDes = []
        self.ItemUse = []
        self.UseSound = []
        self.ItemSound = []
        self.Ammo = []
        self.ItemArt = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "Items", attrs, None, [])

class Mono_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'Building', u'Room']
        Q2API.xml.base_xml.XMLNode.__init__(self, "Mono", attrs, None, [])

class Monster_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'Building', u'Room']
        self.MonsterArt = []
        self.MonsterAttack = []
        self.MonsterDes = []
        self.BattleMusic = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "Monster", attrs, None, [])

class Req_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'Building', u'Room']
        self.ReqSound = []
        self.ReqMes = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "Req", attrs, None, [])

class Sound_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'Building', u'Room']
        Q2API.xml.base_xml.XMLNode.__init__(self, "Sound", attrs, None, [])

class Room_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 2
        self.path = [None, u'Building']
        self.Sound = []
        self.Req = []
        self.Exit = []
        self.Monster = []
        self.Mono = []
        self.Items = []
        self.Des = []
        self.Art = []
        self.Event = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "Room", attrs, None, [])

class Building_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 1
        self.path = [None]
        self.Room = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "Building", attrs, None, [])

class NodeHandler(xml.sax.handler.ContentHandler):
    """SAX ContentHandler to map XML input class/object"""
    def __init__(self, return_q):     # overridden in subclass
        self.obj_depth = [None]
        self.return_q = return_q
        self.last_processed = None
        self.char_buffer = []
        xml.sax.handler.ContentHandler.__init__(self)   # superclass init

    def startElement(self, name, attrs): # creating the node along the path being tracked
        """Override base class ContentHandler method"""
        name = clean_node_name(name)
        p_attrs = process_attrs(attrs)

        if name == "":
            raise ValueError, "XML Node name cannot be empty"

        elif name == "Sound":
            self.obj_depth.append(Sound_q2class(p_attrs))

        elif name == "MonsterArt":
            self.obj_depth.append(MonsterArt_q2class(p_attrs))

        elif name == "ItemDes":
            self.obj_depth.append(ItemDes_q2class(p_attrs))

        elif name == "Req":
            self.obj_depth.append(Req_q2class(p_attrs))

        elif name == "Exit":
            self.obj_depth.append(Exit_q2class(p_attrs))

        elif name == "ItemUse":
            self.obj_depth.append(ItemUse_q2class(p_attrs))

        elif name == "Monster":
            self.obj_depth.append(Monster_q2class(p_attrs))

        elif name == "MonsterAttack":
            self.obj_depth.append(MonsterAttack_q2class(p_attrs))

        elif name == "UseSound":
            self.obj_depth.append(UseSound_q2class(p_attrs))

        elif name == "MonsterDes":
            self.obj_depth.append(MonsterDes_q2class(p_attrs))

        elif name == "Mono":
            self.obj_depth.append(Mono_q2class(p_attrs))

        elif name == "ItemSound":
            self.obj_depth.append(ItemSound_q2class(p_attrs))

        elif name == "Building":
            self.obj_depth.append(Building_q2class(p_attrs))

        elif name == "Room":
            self.obj_depth.append(Room_q2class(p_attrs))

        elif name == "BattleMusic":
            self.obj_depth.append(BattleMusic_q2class(p_attrs))

        elif name == "Items":
            self.obj_depth.append(Items_q2class(p_attrs))

        elif name == "Des":
            self.obj_depth.append(Des_q2class(p_attrs))

        elif name == "Ammo":
            self.obj_depth.append(Ammo_q2class(p_attrs))

        elif name == "Art":
            self.obj_depth.append(Art_q2class(p_attrs))

        elif name == "ItemArt":
            self.obj_depth.append(ItemArt_q2class(p_attrs))

        elif name == "ReqSound":
            self.obj_depth.append(ReqSound_q2class(p_attrs))

        elif name == "ReqMes":
            self.obj_depth.append(ReqMes_q2class(p_attrs))

        elif name == "Event":
            self.obj_depth.append(Event_q2class(p_attrs))

        self.char_buffer = []
        self.last_processed = "start"

    def endElement(self, name): # need to append the node that is closing in the right place
        """Override base class ContentHandler method"""
        name = clean_node_name(name)

        if (len(self.char_buffer) != 0) and (self.last_processed == "start"):
            self.obj_depth[-1].value = "".join(self.char_buffer)

        if name == "":
            raise ValueError, "XML Node name cannot be empty"

        elif name == "Sound":
            self.obj_depth[-2].Sound.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "MonsterArt":
            self.obj_depth[-2].MonsterArt.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "ItemDes":
            self.obj_depth[-2].ItemDes.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "Req":
            self.obj_depth[-2].Req.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "Exit":
            self.obj_depth[-2].Exit.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "ItemUse":
            self.obj_depth[-2].ItemUse.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "Monster":
            self.obj_depth[-2].Monster.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "MonsterAttack":
            self.obj_depth[-2].MonsterAttack.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "UseSound":
            self.obj_depth[-2].UseSound.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "MonsterDes":
            self.obj_depth[-2].MonsterDes.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "Mono":
            self.obj_depth[-2].Mono.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "ItemSound":
            self.obj_depth[-2].ItemSound.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "Building":
            # root node is not added to a parent; stays on the "stack" for the return_object
            self.char_buffer = []
            self.last_processed = "end"
            return

        elif name == "Room":
            self.obj_depth[-2].Room.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "BattleMusic":
            self.obj_depth[-2].BattleMusic.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "Items":
            self.obj_depth[-2].Items.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "Des":
            self.obj_depth[-2].Des.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "Ammo":
            self.obj_depth[-2].Ammo.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "Art":
            self.obj_depth[-2].Art.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "ItemArt":
            self.obj_depth[-2].ItemArt.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "ReqSound":
            self.obj_depth[-2].ReqSound.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "ReqMes":
            self.obj_depth[-2].ReqMes.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "Event":
            self.obj_depth[-2].Event.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        self.last_processed = "end"


    def characters(self, in_chars):
        """Override base class ContentHandler method"""
        self.char_buffer.append(in_chars)

    def endDocument(self):
        """Override base class ContentHandler method"""
        self.return_q.put(self.obj_depth[-1])

def obj_wrapper(xml_stream):
    """Call the handler against the XML, then get the returned object and pass it back up"""
    try:
        return_q = Queue.Queue()
        xml.sax.parseString(xml_stream, NodeHandler(return_q))
        return (True, return_q.get())
    except Exception, e:
        return (False, (Exception, e))


