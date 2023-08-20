# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service
import ipaddress


# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        vars = ncs.template.Variables()
        template = ncs.template.Template(service)
        index = 10
        for rule in service.rule:
            # source
            try:
                source = ipaddress.ip_address(rule.source.address)
                source_text = f"host {source}"
            except:
                source = ipaddress.ip_network(rule.source.address)
                source_wildcard_mask = ipaddress.ip_address(int(source.netmask)^(2**32-1))
                source_text = f"{source.network_address} {source_wildcard_mask}"
            
            if rule.source.port:
                source_port_text = f" eq {rule.source.port}"
            else:
                source_port_text = ""
            #destination
            try:
                destination = ipaddress.ip_address(rule.destination.address)
                destination_text = f"host {destination}"
            except:
                destination = ipaddress.ip_network(rule.destination.address)
                destination_wildcard_mask = ipaddress.ip_address(int(destination.netmask)^(2**32-1))
                destination_text = f"{destination.network_address} {destination_wildcard_mask}"

            if rule.log:
                log_text = f" log"
            else:
                log_text = ""

            rule_text = f"{index} remark Rule {rule.name} in ACL Service {service.name}"
            vars.add("rule_text", rule_text)
            template.apply('acl-service-template', vars)
            index += 1
            if rule.description:
                rule_text = f"{index} remark {rule.description}"
                vars.add("rule_text", rule_text)
                template.apply('acl-service-template', vars)
                index += 1
            rule_text = f"{index} {rule.action} {rule.protocol} {source_text}{source_port_text} {destination_text} eq {rule.destination.port}{log_text}"
            vars.add("rule_text", rule_text)
            template.apply('acl-service-template', vars)
            index += 1


    # The pre_modification() and post_modification() callbacks are optional,
    # and are invoked outside FASTMAP. pre_modification() is invoked before
    # create, update, or delete of the service, as indicated by the enum
    # ncs_service_operation op parameter. Conversely
    # post_modification() is invoked after create, update, or delete
    # of the service. These functions can be useful e.g. for
    # allocations that should be stored and existing also when the
    # service instance is removed.

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service postmod(service=', kp, ')')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('acl-service-servicepoint', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
