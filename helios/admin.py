from django.contrib import admin
from helios.models import CastVote, Election, Trustee


class ElectionAdmin(admin.ModelAdmin):
	fields = ('admin', 'short_name', 'name', 'election_type',
	'openreg', 'use_voter_aliases', 'randomize_answer_order', 
	'frozen_at', 'tallying_started_at', 'tallying_finished_at',
	'help_email', 'election_info_url', 'result', 'featured_p')
	readonly_fields = ('admin', 'short_name', 'name', 'election_type',
	'openreg', 'use_voter_aliases', 'randomize_answer_order', 
	'frozen_at', 'tallying_started_at', 'tallying_finished_at', 'help_email',
	'election_info_url', 'result')
	list_display = ('admin', 'name', 'election_type', 'featured_p')


class TrusteeAdmin(admin.ModelAdmin):	
	readonly_fields = ('uuid', 'election','name', 'email', 'secret',)
	list_display = ('uuid', 'election', 'name', 'email', 'secret',)


admin.site.register(Election, ElectionAdmin)
admin.site.register(Trustee, TrusteeAdmin)
