"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment


class TotemOTR_JIDInput(XBlock):
    """
    Waits for student to input Jabber ID, establishes shared state with Mcabber which will initiate an OTR session.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>

    jid = String(
        default=None, scope=Scope.user_state,
        help="The user's jabber id",
    )

    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )


    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # Display the XBlock interface to the student.
    def student_view(self, context=None):
        """
        The primary view of the TotemOTRXBlock, shown to students
        when viewing courses.
        """
        #
	# Display the HTML input box for the jid.
        html = self.resource_string("static/html/totem_otr.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/totem_otr.css"))
        frag.add_javascript(self.resource_string("static/js/src/totem_otr.js"))
        frag.initialize_js('TotemOTRXBlock')
        return frag

    # Handlers for frontend Javascript.
    @XBlock.json_handler
    def submit_jid(self, data, suffix=''):
        """
        User created their jabber account and let us know which it is. We use this to bootstrap shared state with mcabber.
	"""
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    @XBlock.json_handler
    def poll_state(self, data, suffix=''):
        """
        Ajax polling to see the progress state for the user. 
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

class TotemOTR_Trust(XBlock):
    """
    Waits for student to initiate SMP shared secret verification.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>

    jid = String(
        default=None, scope=Scope.user_state,
        help="The user's jabber id",
    )

    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )


    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # Display the XBlock interface to the student.
    def student_view(self, context=None):
        """
        The primary view of the TotemOTRXBlock, shown to students
        when viewing courses.
        """
        #
	# Display the HTML input box for the jid.
        html = self.resource_string("static/html/totem_otr.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/totem_otr.css"))
        frag.add_javascript(self.resource_string("static/js/src/totem_otr.js"))
        frag.initialize_js('TotemOTRXBlock')
        return frag

    # Handlers for frontend Javascript.
    @XBlock.json_handler
    def submit_jid(self, data, suffix=''):
        """
        User created their jabber account and let us know which it is. We use this to bootstrap shared state with mcabber.
	"""
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    @XBlock.json_handler
    def poll_state(self, data, suffix=''):
        """
        Ajax polling to see the progress state for the user. 
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

   # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("TotemOTRXBlock",
             """<vertical_demo>
                <totem_otr/>
                </vertical_demo>
             """),
        ]
