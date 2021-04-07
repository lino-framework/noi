# -*- coding: UTF-8 -*-
# Copyright 2016 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""This is a real-world example of how the application developer
can provide automatic data migrations for :ref:`dpy`.

This module is used because a :ref:`noi` Site has
:attr:`migration_class <lino.core.site.Site.migration_class>` set to
``"lino_noi.lib.migrate.Migrator"``.

"""

from django.conf import settings
from lino.api import dd, rt
from lino.utils.dpy import Migrator, override
from lino.utils.dpy import create_mti_child


def noop(*args):
    return None


class Migrator(Migrator):
    "The standard migrator for :ref:`noi`."

    def migrate_from_0_0_1(self, globals_dict):
        """
        - Convert products to topics.
        - Interest.product becomes Interest.topic
        - Interest.site.partner becomes Interest.partner and if the site has
          no partner, create one.
        - Rename Faculty.product_cat to topic_group
        - Rename Competence.product to Competence.topic
           
        """

        bv2kw = globals_dict['bv2kw']
        products_Product = rt.models.topics.Topic
        products_Category = rt.models.topics.TopicGroup
        faculties_Competence = rt.models.faculties.Competence
        faculties_Faculty = rt.models.faculties.Faculty
        tickets_Site = rt.models.tickets.Site
        tickets_Interest = rt.models.topics.Interest
        tickets_Ticket = rt.models.tickets.Ticket
        Partner = dd.resolve_model(dd.plugins.topics.partner_model)

        @override(globals_dict)
        def create_tickets_site(id, partner_id, name, remark):
            kw = dict()
            kw.update(id=id)
            kw.update(partner_id=partner_id)
            kw.update(name=name)
            kw.update(remark=remark)
            return tickets_Site(**kw)

        @override(globals_dict)
        def create_tickets_interest(id, product_id, site_id):
            kw = dict()
            kw.update(id=id)
            kw.update(topic_id=product_id)
            try:
                partner = Partner.objects.get(id=site_id)
            except Partner.DoesNotExist:
                partner = Partner(id=site_id, name=str(site_id))
                partner.save()
            kw.update(partner=partner)
            return tickets_Interest(**kw)

        @override(globals_dict)
        def create_products_productcat(id, name, description):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name', name))
            kw.update(description=description)
            return products_Category(**kw)

        @override(globals_dict)
        def create_products_product(id, ref, name, description, category_id):
            kw = dict()
            kw.update(id=id)
            kw.update(ref=ref)
            if name is not None: kw.update(bv2kw('name', name))
            if description is not None: kw.update(bv2kw('description', description))
            kw.update(topic_group_id=category_id)
            return products_Product(**kw)

        @override(globals_dict)
        def create_tickets_ticket(id, modified, created, closed, private, planned_time, project_id, site_id, product_id,
                                  nickname, summary, description, upgrade_notes, ticket_type_id, duplicate_of_id,
                                  reported_for_id, fixed_for_id, assigned_to_id, reporter_id, state, waiting_for,
                                  deadline, priority, feedback, standby, faculty_id):
            if state: state = settings.SITE.models.tickets.TicketStates.get_by_value(state)
            kw = dict()
            kw.update(id=id)
            kw.update(modified=modified)
            kw.update(created=created)
            kw.update(closed=closed)
            kw.update(private=private)
            kw.update(planned_time=planned_time)
            kw.update(project_id=project_id)
            kw.update(site_id=site_id)
            kw.update(topic_id=product_id)
            kw.update(nickname=nickname)
            kw.update(summary=summary)
            kw.update(description=description)
            kw.update(upgrade_notes=upgrade_notes)
            kw.update(ticket_type_id=ticket_type_id)
            kw.update(duplicate_of_id=duplicate_of_id)
            kw.update(reported_for_id=reported_for_id)
            kw.update(fixed_for_id=fixed_for_id)
            kw.update(assigned_to_id=assigned_to_id)
            kw.update(reporter_id=reporter_id)
            kw.update(state=state)
            kw.update(waiting_for=waiting_for)
            kw.update(deadline=deadline)
            kw.update(priority=priority)
            kw.update(feedback=feedback)
            kw.update(standby=standby)
            kw.update(faculty_id=faculty_id)
            return tickets_Ticket(**kw)

        @override(globals_dict)
        def create_faculties_competence(id, seqno, user_id, faculty_id, affinity, product_id):
            kw = dict()
            kw.update(id=id)
            kw.update(seqno=seqno)
            kw.update(user_id=user_id)
            kw.update(faculty_id=faculty_id)
            kw.update(affinity=affinity)
            kw.update(topic_id=product_id)
            return faculties_Competence(**kw)

        @override(globals_dict)
        def create_faculties_faculty(id, ref, parent_id, name, affinity, product_cat_id):
            kw = dict()
            kw.update(id=id)
            kw.update(ref=ref)
            kw.update(parent_id=parent_id)
            if name is not None: kw.update(bv2kw('name', name))
            kw.update(affinity=affinity)
            kw.update(topic_group_id=product_cat_id)
            return faculties_Faculty(**kw)

        return '0.0.2'

    def migrate_from_0_0_2(self, globals_dict):

        bv2kw = globals_dict['bv2kw']
        faculties_Faculty = rt.models.faculties.Faculty
        tickets_Site = rt.models.tickets.Site

        @override(globals_dict)
        def create_faculties_faculty(id, ref, seqno, parent_id, name, affinity, product_cat_id):
            kw = dict()
            kw.update(id=id)
            # kw.update(ref=ref)
            kw.update(seqno=seqno)
            kw.update(parent_id=parent_id)
            if name is not None: kw.update(bv2kw('name', name))
            kw.update(affinity=affinity)
            # kw.update(product_cat_id=product_cat_id)
            return faculties_Faculty(**kw)

        @override(globals_dict)
        def create_tickets_site(id, partner_id, name, remark):
            kw = dict()
            kw.update(id=id)
            # kw.update(partner_id=partner_id)
            kw.update(name=name)
            kw.update(remark=remark)
            return tickets_Site(**kw)

        return '0.0.3'

    def migrate_from_1_0_1(self, globals_dict):
        """Move Deployment and Milestone from 'tickets' to new plugin
        'deploy'.

        """
        if settings.SITE.is_installed('deploy'):
            globals_dict.update(
                tickets_Deployment=rt.models.deploy.Deployment)
            globals_dict.update(
                tickets_Milestone=rt.models.deploy.Milestone)
        else:
            globals_dict.update(create_tickets_deployment=noop)
            globals_dict.update(create_tickets_milestone=noop)
        return '1.0.2'

    def migrate_from_1_0_2(self, globals_dict):
        """
        - convert stars.Star to votes.Vote
        
        """
        from django.utils import timezone
        # bv2kw = globals_dict['bv2kw']
        new_content_type_id = globals_dict['new_content_type_id']
        # cal_EventType = resolve_model("cal.EventType")
        # users.User = resolve_model("users.User")
        votes_Vote = rt.models.votes.Vote
        tickets_Ticket = rt.models.tickets.Ticket

        @override(globals_dict)
        def create_stars_star(id, user_id, owner_type_id, owner_id, nickname):
            # owner_type_id = new_content_type_id(owner_type_id)
            kw = dict()
            kw.update(id=id)
            kw.update(user_id=user_id)
            # kw.update(owner_type_id=owner_type_id)
            kw.update(created=timezone.now())
            kw.update(votable_id=owner_id)
            kw.update(nickname=nickname)
            return votes_Vote(**kw)

        # @override(globals_dict)
        # def create_tickets_ticket(id, modified, created, assigned_to_id, closed, private, planned_time, project_id, site_id, topic_id, nickname, summary, description, upgrade_notes,
        #     ticket_type_id, duplicate_of_id, reporter_id, state, rating, waiting_for, deadline,
        #     priority, feedback, standby, faculty_id):
        #     if state: state = settings.SITE.models.tickets.TicketStates.get_by_value(state)
        #     if rating: rating = settings.SITE.models.tickets.Ratings.get_by_value(rating)
        #     kw = dict()
        #     kw.update(id=id)
        #     kw.update(modified=modified)
        #     kw.update(created=created)
        #     # kw.update(assigned_to_id=assigned_to_id)
        #     kw.update(closed=closed)
        #     kw.update(private=private)
        #     kw.update(planned_time=planned_time)
        #     kw.update(project_id=project_id)
        #     kw.update(site_id=site_id)
        #     kw.update(topic_id=topic_id)
        #     kw.update(nickname=nickname)
        #     kw.update(summary=summary)
        #     kw.update(description=description)
        #     kw.update(upgrade_notes=upgrade_notes)
        #     kw.update(ticket_type_id=ticket_type_id)
        #     kw.update(duplicate_of_id=duplicate_of_id)
        #     kw.update(reporter_id=reporter_id)
        #     kw.update(state=state)
        #     # kw.update(rating=rating)
        #     kw.update(waiting_for=waiting_for)
        #     kw.update(deadline=deadline)
        #     kw.update(priority=priority)
        #     kw.update(feedback=feedback)
        #     kw.update(standby=standby)
        #     kw.update(faculty_id=faculty_id)
        #     return tickets_Ticket(**kw)

        return '2016.12.0'

    def unused_migrate_from_2016_12_0(self, globals_dict):
        """
        - convert Ticket.assigned_to to votes
        
        """
        votes_Vote = rt.models.votes.Vote
        tickets_Ticket = rt.models.tickets.Ticket

        @override(globals_dict)
        def create_tickets_ticket(id, modified, created, assigned_to_id, closed, private, planned_time, project_id,
                                  site_id, topic_id, nickname, summary, description, upgrade_notes, ticket_type_id,
                                  duplicate_of_id, reported_for_id, fixed_for_id, reporter_id, state, waiting_for,
                                  deadline, priority, feedback, standby, faculty_id):
            if state: state = settings.SITE.models.tickets.TicketStates.get_by_value(state)
            kw = dict()
            kw.update(id=id)
            kw.update(modified=modified)
            kw.update(created=created)
            # kw.update(assigned_to_id=assigned_to_id)
            kw.update(closed=closed)
            kw.update(private=private)
            kw.update(planned_time=planned_time)
            kw.update(project_id=project_id)
            kw.update(site_id=site_id)
            kw.update(topic_id=topic_id)
            kw.update(nickname=nickname)
            kw.update(summary=summary)
            kw.update(description=description)
            kw.update(upgrade_notes=upgrade_notes)
            kw.update(ticket_type_id=ticket_type_id)
            kw.update(duplicate_of_id=duplicate_of_id)
            kw.update(reported_for_id=reported_for_id)
            kw.update(fixed_for_id=fixed_for_id)
            kw.update(reporter_id=reporter_id)
            kw.update(state=state)
            kw.update(waiting_for=waiting_for)
            kw.update(deadline=deadline)
            kw.update(priority=priority)
            kw.update(feedback=feedback)
            kw.update(standby=standby)
            kw.update(faculty_id=faculty_id)
            ticket = tickets_Ticket(**kw)
            if not assigned_to_id:
                return ticket
            vote = votes_Vote(
                votable=ticket, user_id=assigned_to_id, created=created,
                state=settings.SITE.models.votes.VoteStates.assigned)
            return (ticket, vote)

        return '2016.12.1'

    def migrate_from_2016_12_1(self, globals_dict):
        """
        - faculties.Faculty.faculty_type -> faculties.Faculty.skill_type
        - users.User now an MTI child of contacts.Person
        - convert Tickets.faculty to faculty.Demand instance
        
        """
        PARTNER_OFFSET = 200
        bv2kw = globals_dict['bv2kw']
        users.User = rt.models.users.User
        # votes_Vote = rt.models.votes.Vote
        tickets_Ticket = rt.models.tickets.Ticket
        tickets_Site = rt.models.tickets.Site
        tickets_Project = rt.models.tickets.Project
        faculties_Faculty = rt.models.faculties.Faculty
        faculties_Demand = rt.models.faculties.Demand
        # contacts_Person = rt.models.contacts.Person
        topics_Interest = rt.models.topics.Interest
        contacts_Role = rt.models.contacts.Role

        def offset_factory(orig):
            def f(partner_id, *args):
                partner_id = str(int(partner_id) + PARTNER_OFFSET)
                return orig(partner_id, *args)
            return f

        for k in ('create_contacts_partner', 'create_contacts_person', 'create_contacts_company'):
            globals_dict[k] = offset_factory(globals_dict[k])

        # globals_dict.update(create_contacts_partner=offset_factory(create_contacts_partner))
        # globals_dict.update(create_contacts_person=offset_factory(create_contacts_person))
        # globals_dict.update(create_contacts_company=offset_factory(create_contacts_company))
        # globals_dict.update(create_contacts_person=noop)
        # globals_dict.update(create_contacts_company=noop)
        # globals_dict.update(create_contacts_role=noop)
        # globals_dict.update(create_topics_interest=noop)
        # globals_dict.update(create_deploy_deployment=noop)
        # globals_dict.update(create_deploy_milestone=noop)

        @override(globals_dict)
        def create_topics_interest(id, topic_id, partner_id):
            kw = dict()
            kw.update(id=id)
            kw.update(topic_id=topic_id)
            if partner_id:
                partner_id = str(int(partner_id) + PARTNER_OFFSET)
            kw.update(partner_id=partner_id)
            return topics_Interest(**kw)

        @override(globals_dict)
        def create_tickets_project(id, ref, parent_id, start_date, end_date, company_id, contact_person_id, contact_role_id, private, closed, planned_time, name, assign_to_id, type_id, description, srcref_url_template, changeset_url_template):
            kw = dict()
            kw.update(id=id)
            kw.update(ref=ref)
            kw.update(parent_id=parent_id)
            kw.update(start_date=start_date)
            kw.update(end_date=end_date)
            if contact_person_id:
                contact_person_id = str(int(contact_person_id) + PARTNER_OFFSET)
            if company_id:
                company_id = str(int(company_id) + PARTNER_OFFSET)
            kw.update(company_id=company_id)
            kw.update(contact_person_id=contact_person_id)
            kw.update(contact_role_id=contact_role_id)
            kw.update(private=private)
            kw.update(closed=closed)
            kw.update(planned_time=planned_time)
            kw.update(name=name)
            kw.update(assign_to_id=assign_to_id)
            kw.update(type_id=type_id)
            kw.update(description=description)
            kw.update(srcref_url_template=srcref_url_template)
            kw.update(changeset_url_template=changeset_url_template)
            return tickets_Project(**kw)

        # @override(globals_dict)
        # def create_tickets_site(id, partner_id, name, remark):
        #     kw = dict()
        #     kw.update(id=id)
        #     if partner_id:
        #         partner_id = str(int(partner_id) + PARTNER_OFFSET)
        #     kw.update(partner_id=partner_id)
        #     kw.update(name=name)
        #     kw.update(remark=remark)
        #     return tickets_Site(**kw)

        @override(globals_dict)
        def create_contacts_role(id, type_id, person_id, company_id):
            kw = dict()
            kw.update(id=id)
            kw.update(type_id=type_id)
            if person_id:
                person_id = str(int(person_id) + PARTNER_OFFSET)
            if company_id:
                company_id = str(int(company_id) + PARTNER_OFFSET)
            kw.update(person_id=person_id)
            kw.update(company_id=company_id)
            return contacts_Role(**kw)

        # @override(globals_dict)
        # def create_faculties_faculty(id, seqno, parent_id, name, affinity, faculty_type_id, remarks):
        #     kw = dict()
        #     kw.update(id=id)
        #     kw.update(seqno=seqno)
        #     kw.update(parent_id=parent_id)
        #     if name is not None: kw.update(bv2kw('name',name))
        #     kw.update(affinity=affinity)
        #     # kw.update(faculty_type_id=faculty_type_id)
        #     kw.update(skill_type_id=faculty_type_id)
        #     kw.update(remarks=remarks)
        #     return faculties_Faculty(**kw)


        # @override(globals_dict)
        # def create_users_user(id, email, language, url, phone, gsm, fax, modified, created, country_id, city_id, zip_code, region_id, addr1, street_prefix, street, street_no, street_box, addr2, password, last_login, timezone, username, user_type, initials, first_name, last_name, remarks, partner_id, callme_mode, verification_code, user_state, user_site_id, open_session_on_new_ticket, notify_myself, mail_mode):
        #     if profile: profile = settings.SITE.models.users.UserTypes.get_by_value(profile)
        #     if user_state: user_state = settings.SITE.models.users.UserStates.get_by_value(user_state)
        #     if mail_mode: mail_mode = settings.SITE.models.notify.MailModes.get_by_value(mail_mode)
        #     # if contacts_Partner.objects.exists(id=id):
        #     # return create_mti_child(contacts_Person, id, users.User,modified=modified,created=created,password=password,last_login=last_login,timezone=timezone,username=username,profile=profile,initials=initials,partner_id=partner_id,callme_mode=callme_mode,verification_code=verification_code,user_state=user_state,open_session_on_new_ticket=open_session_on_new_ticket,notify_myself=notify_myself,mail_mode=mail_mode)
            
        #     kw = dict()
        #     kw.update(id=id)
        #     kw.update(email=email)
        #     kw.update(language=language)
        #     kw.update(url=url)
        #     kw.update(phone=phone)
        #     kw.update(gsm=gsm)
        #     kw.update(fax=fax)
        #     kw.update(modified=modified)
        #     kw.update(created=created)
        #     kw.update(country_id=country_id)
        #     kw.update(city_id=city_id)
        #     kw.update(zip_code=zip_code)
        #     kw.update(region_id=region_id)
        #     kw.update(addr1=addr1)
        #     kw.update(street_prefix=street_prefix)
        #     kw.update(street=street)
        #     kw.update(street_no=street_no)
        #     kw.update(street_box=street_box)
        #     kw.update(addr2=addr2)
        #     kw.update(password=password)
        #     kw.update(last_login=last_login)
        #     kw.update(timezone=timezone)
        #     kw.update(username=username)
        #     kw.update(name=username)  #
        #     kw.update(profile=profile)
        #     kw.update(initials=initials)
        #     kw.update(first_name=first_name)
        #     kw.update(last_name=last_name)
        #     kw.update(remarks=remarks)
        #     # kw.update(partner_id=partner_id)
        #     kw.update(callme_mode=callme_mode)
        #     kw.update(verification_code=verification_code)
        #     kw.update(user_state=user_state)
        #     # kw.update(user_site_id=user_site_id)
        #     kw.update(open_session_on_new_ticket=open_session_on_new_ticket)
        #     kw.update(notify_myself=notify_myself)
        #     kw.update(mail_mode=mail_mode)
        #     return users_User(**kw)

        @override(globals_dict)
        def create_tickets_ticket(id, modified, created, user_id, private, closed, planned_time, project_id, site_id, topic_id, nickname, summary, description, upgrade_notes, ticket_type_id, duplicate_of_id, reported_for_id, fixed_for_id, reporter_id, end_user_id, state, waiting_for, deadline, priority, feedback, standby, faculty_id):
            if state: state = settings.SITE.models.tickets.TicketStates.get_by_value(state)
            kw = dict()
            kw.update(id=id)
            kw.update(modified=modified)
            kw.update(created=created)
            kw.update(user_id=user_id)
            kw.update(private=private)
            kw.update(closed=closed)
            kw.update(planned_time=planned_time)
            kw.update(project_id=project_id)
            kw.update(site_id=site_id)
            kw.update(topic_id=topic_id)
            # kw.update(nickname=nickname)
            kw.update(summary=summary)
            kw.update(description=description)
            kw.update(upgrade_notes=upgrade_notes)
            kw.update(ticket_type_id=ticket_type_id)
            kw.update(duplicate_of_id=duplicate_of_id)
            # kw.update(reported_for_id=reported_for_id)
            # kw.update(fixed_for_id=fixed_for_id)
            kw.update(reporter_id=reporter_id)
            kw.update(end_user_id=end_user_id)
            kw.update(state=state)
            kw.update(waiting_for=waiting_for)
            kw.update(deadline=deadline)
            kw.update(priority=priority)
            kw.update(feedback=feedback)
            kw.update(standby=standby)
            yield tickets_Ticket(**kw)
            # kw.update(faculty_id=faculty_id)
            if faculty_id:
                yield faculties_Demand(demander_id=id, skill_id=faculty_id)

        return '2017.02.0'

