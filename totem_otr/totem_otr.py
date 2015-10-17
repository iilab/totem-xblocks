"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources, hmac, hashlib, os, sys, string, random

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment

basepath = '/opt/totem-bots'

class TotemOTRXBlock(XBlock):
    """
    Waits for student to input Jabber ID, establishes shared state with Mcabber which will initiate an OTR session.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>

    jid = String(
        default=None, scope=Scope.user_state,
        help="The user's jabber id",
    )

    learner_hash = String(
        default='', scope=Scope.user_state,
        help="Learner Hash",
    )

    smp_secret = String(
        default='', scope=Scope.user_state,
        help="SMP Secret",
    )

    secret = String(
        default='', scope=Scope.user_state,
        help="Secret",
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

        with open('%s/secret' % basepath ,'r') as f:
            self.secret=f.read().strip()

        #
    	# Display the HTML input box for the jid.
        #    html = self.resource_string("static/html/totem_otr.html")

        html = u"""
                <input class='jid' type='text' name='input' value='{self.jid}'/>
                <input type='button' class='submit' value='Submit!'/>
                <br />
                <span class='message'></span>
                """.format(self=self)

        frag = Fragment(html)
    #    frag.add_css(self.resource_string("static/css/totem_otr.css"))
        frag.add_javascript("""
            function TotemOTRXBlock(runtime, element) {

                function shareSMP(result) {
                    $('.message', element).text('Well done! Use this as our shared "secret: "'+result['smp_secret']);
                }

                var handlerUrl = runtime.handlerUrl(element, 'submit_jid');

                $('.submit', element).click(function(eventObject) {
                    $.ajax({
                        type: "POST",
                        url: handlerUrl,
                        data: JSON.stringify({"jid": $('.jid').val()}),
                        success: shareSMP
                    });
                });

                $(function ($) {
                    /* Here's where you'd do things on page load. */
                });
            }
        """)
    #    frag.add_javascript(self.resource_string("static/js/src/totem_otr.js"))
        frag.initialize_js('TotemOTRXBlock')
        return frag

    # Handlers for frontend Javascript.
    @XBlock.json_handler
    def submit_jid(self, data, suffix=''):
        """
        User created their jabber account and let us know which it is. We use this to bootstrap shared state with mcabber.
    	"""
        # Just to show data coming in...
        # assert data['hello'] == 'world'
       
        self.jid = data['jid']
        self.learner_hash = hmac.new(str(self.secret), str(self.jid), hashlib.sha256).hexdigest()

        self.smp_secret=''.join(random.choice(string.ascii_uppercase +
            string.digits + string.ascii_lowercase) for _ in range(32))

        with open('%s/data/%s/smpsecret' % (basepath,self.learner_hash), 'w+') as fd:
            fd.write(self.smp_secret)

	msg = "Hi %s! Thanks for using Totem. How are you today?" % (self.jid.split('@')[0])

        with open('%s/otr/mcabber.fifo' % basepath, 'a') as fd:
            # start OTR
            fd.write("otr start %s\n" % (self.jid))
            # greet student
            fd.write("say_to -q %s %s\n" % (self.jid, msg))
            fd.write('say_to -q %s Now please initiate the SMP dance using the shared "secret" shown in the web browser\n' % (self.jid))

        return { "learner_hash": self.learner_hash, 
                 "secret": str(self.secret),
                 "jid": str(self.jid),
                 "smp_secret": str(self.smp_secret),
               }

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
                   <html_demo>
                        <p>Please install an instant messaging client which supports OTR and follow these steps:</p>
                        <ol>
                            <li>Create a Jabber account and paste your Jabber ID in the first field.</li>
                            <li>Verify that the OTR encrypted session has started.</li>
                            <li>Establish trust by verifying the identity of totem@jabber.ccc.de with a shared secret.</li>
                        </ol>
                    </html_demo>
                    <totem_otr_status/>
                    <totem_otr/>
                </vertical_demo>
             """),
        ]

class StatusBlock(XBlock):
    """
    Show shared state.
    """

    def student_view(self, context=None):  # pylint: disable=W0613
        """Provide default student view."""
        # Get the attempts for all problems in my parent.
        if self.parent:
            # TODO: Get shared state from data folder.
            #
            
            content = u"No state..."

            # these two lines are equivalent, and both work:
            # attempts = list(self.runtime.query(self).parent().descendants().attr("problem_attempted"))
            # attempts = list(self.runtime.querypath(self, "..//@problem_attempted"))
            # num_problems = len(attempts)
            # attempted = sum(attempts)
            # if num_problems == 0:
            #     content = u"There are no problems here..."
            # elif attempted == num_problems:
            #     content = u"Great! You attempted all %d problems!" % num_problems
            # else:
            #     content = u"Hmm, you've only tried %d out of %d problems..." % (attempted, num_problems)
        else:
            content = u"I have nothing to live for! :("
        return Fragment(content)

# class TotemOTR_Trust(XBlock):
#     """
#     Waits for student to initiate SMP shared secret verification.
#     """

#     # Fields are defined on the class.  You can access them in your code as
#     # self.<fieldname>

#     jid = String(
#         default=None, scope=Scope.user_state,
#         help="The user's jabber id",
#     )

#     count = Integer(
#         default=0, scope=Scope.user_state,
#         help="A simple counter, to show something happening",
#     )


#     def resource_string(self, path):
#         """Handy helper for getting resources from our kit."""
#         data = pkg_resources.resource_string(__name__, path)
#         return data.decode("utf8")

#     # Display the XBlock interface to the student.
#     def student_view(self, context=None):
#         """
#         The primary view of the TotemOTRXBlock, shown to students
#         when viewing courses.
#         """
#         #
# 	# Display the HTML input box for the jid.
#         html = self.resource_string("static/html/totem_otr.html")
#         frag = Fragment(html.format(self=self))
#         frag.add_css(self.resource_string("static/css/totem_otr.css"))
#         frag.add_javascript(self.resource_string("static/js/src/totem_otr.js"))
#         frag.initialize_js('TotemOTRXBlock')
#         return frag

#     # Handlers for frontend Javascript.
#     @XBlock.json_handler
#     def submit_jid(self, data, suffix=''):
#         """
#         User created their jabber account and let us know which it is. We use this to bootstrap shared state with mcabber.
# 	"""
#         # Just to show data coming in...
#         assert data['hello'] == 'world'

#         self.count += 1
#         return {"count": self.count}

#     @XBlock.json_handler
#     def poll_state(self, data, suffix=''):
#         """
#         Ajax polling to see the progress state for the user. 
#         """
#         # Just to show data coming in...
#         assert data['hello'] == 'world'

#         self.count += 1
#         return {"count": self.count}
