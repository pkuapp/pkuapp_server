# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'place'
        db.create_table('Server_place', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('interid', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('keyid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('roomtype', self.gf('django.db.models.fields.CharField')(max_length=5, null=True)),
            ('rcapacity', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('feedback', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('feedbacktime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal('Server', ['place'])

        # Adding model 'School'
        db.create_table('Server_school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('ename', self.gf('django.db.models.fields.CharField')(max_length=75)),
        ))
        db.send_create_signal('Server', ['School'])

        # Adding model 'placet'
        db.create_table('Server_placet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day1', self.gf('django.db.models.fields.IntegerField')()),
            ('day2', self.gf('django.db.models.fields.IntegerField')()),
            ('day3', self.gf('django.db.models.fields.IntegerField')()),
            ('day4', self.gf('django.db.models.fields.IntegerField')()),
            ('day5', self.gf('django.db.models.fields.IntegerField')()),
            ('day6', self.gf('django.db.models.fields.IntegerField')()),
            ('day7', self.gf('django.db.models.fields.IntegerField')()),
            ('weeknumber', self.gf('django.db.models.fields.IntegerField')()),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Server.place'])),
        ))
        db.send_create_signal('Server', ['placet'])

        # Adding model 'teacher'
        db.create_table('Server_teacher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('Server', ['teacher'])

        # Adding model 'course'
        db.create_table('server_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('termnumber', self.gf('django.db.models.fields.IntegerField')()),
            ('courseid', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('keyid', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('classnum', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('rawplace', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('time_test', self.gf('django.db.models.fields.CharField')(max_length=75, null=True)),
            ('credit', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('time', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('day1', self.gf('django.db.models.fields.IntegerField')()),
            ('day2', self.gf('django.db.models.fields.IntegerField')()),
            ('day3', self.gf('django.db.models.fields.IntegerField')()),
            ('day4', self.gf('django.db.models.fields.IntegerField')()),
            ('day5', self.gf('django.db.models.fields.IntegerField')()),
            ('day6', self.gf('django.db.models.fields.IntegerField')()),
            ('day7', self.gf('django.db.models.fields.IntegerField')()),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Server.place'], null=True)),
            ('teachername', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('teacherid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Server.teacher'], null=True)),
            ('course_category', self.gf('django.db.models.fields.IntegerField')()),
            ('Coursetype', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('SchoolCode', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('txType', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('cname', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('ename', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('Server', ['course'])

        # Adding M2M table for field manager on 'course'
        db.create_table('server_course_manager', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['Server.course'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('server_course_manager', ['course_id', 'user_id'])

        # Adding M2M table for field user on 'course'
        db.create_table('server_course_user', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['Server.course'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('server_course_user', ['course_id', 'user_id'])

        # Adding model 'Profile'
        db.create_table('Server_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('realname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('major', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('grade', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('mphone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('user_type', self.gf('django.db.models.fields.IntegerField')()),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('Server', ['Profile'])

        # Adding M2M table for field teach_courses on 'Profile'
        db.create_table('Server_profile_teach_courses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm['Server.profile'], null=False)),
            ('course', models.ForeignKey(orm['Server.course'], null=False))
        ))
        db.create_unique('Server_profile_teach_courses', ['profile_id', 'course_id'])

        # Adding model 'Assignment'
        db.create_table('Server_assignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=755, blank=True)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('tocourse', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Server.course'])),
        ))
        db.send_create_signal('Server', ['Assignment'])

        # Adding model 'comment'
        db.create_table('Server_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Server.course'], null=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Server.place'], null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('sendername', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('Server', ['comment'])

        # Adding model 'sms'
        db.create_table('Server_sms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('sendfrom', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sentsms', to=orm['auth.User'])),
            ('sendername', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('state', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('Server', ['sms'])

        # Adding M2M table for field touser on 'sms'
        db.create_table('Server_sms_touser', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sms', models.ForeignKey(orm['Server.sms'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('Server_sms_touser', ['sms_id', 'user_id'])

        # Adding model 'sys_notice'
        db.create_table('Server_sys_notice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('sendername', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('Server', ['sys_notice'])

        # Adding model 'reply'
        db.create_table('Server_reply', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tocomment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Server.comment'])),
            ('toreply', self.gf('django.db.models.fields.TextField')(null=True)),
            ('touser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('sendfrom', self.gf('django.db.models.fields.related.ForeignKey')(related_name='replys', to=orm['auth.User'])),
            ('sendername', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('Server', ['reply'])

        # Adding model 'notice'
        db.create_table('Server_notice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('touser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('obj_id', self.gf('django.db.models.fields.IntegerField')()),
            ('state', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sendername', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ntype', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('Server', ['notice'])

        # Adding model 'ActivityCategory'
        db.create_table('Server_activitycategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('Server', ['ActivityCategory'])

        # Adding model 'Activity'
        db.create_table('Server_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Server.ActivityCategory'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('organizer', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('Server', ['Activity'])

        # Adding M2M table for field follower on 'Activity'
        db.create_table('Server_activity_follower', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['Server.activity'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('Server_activity_follower', ['activity_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'place'
        db.delete_table('Server_place')

        # Deleting model 'School'
        db.delete_table('Server_school')

        # Deleting model 'placet'
        db.delete_table('Server_placet')

        # Deleting model 'teacher'
        db.delete_table('Server_teacher')

        # Deleting model 'course'
        db.delete_table('server_course')

        # Removing M2M table for field manager on 'course'
        db.delete_table('server_course_manager')

        # Removing M2M table for field user on 'course'
        db.delete_table('server_course_user')

        # Deleting model 'Profile'
        db.delete_table('Server_profile')

        # Removing M2M table for field teach_courses on 'Profile'
        db.delete_table('Server_profile_teach_courses')

        # Deleting model 'Assignment'
        db.delete_table('Server_assignment')

        # Deleting model 'comment'
        db.delete_table('Server_comment')

        # Deleting model 'sms'
        db.delete_table('Server_sms')

        # Removing M2M table for field touser on 'sms'
        db.delete_table('Server_sms_touser')

        # Deleting model 'sys_notice'
        db.delete_table('Server_sys_notice')

        # Deleting model 'reply'
        db.delete_table('Server_reply')

        # Deleting model 'notice'
        db.delete_table('Server_notice')

        # Deleting model 'ActivityCategory'
        db.delete_table('Server_activitycategory')

        # Deleting model 'Activity'
        db.delete_table('Server_activity')

        # Removing M2M table for field follower on 'Activity'
        db.delete_table('Server_activity_follower')


    models = {
        'Server.activity': {
            'Meta': {'object_name': 'Activity'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Server.ActivityCategory']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'follower': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organizer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'Server.activitycategory': {
            'Meta': {'object_name': 'ActivityCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'Server.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '755', 'blank': 'True'}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tocourse': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Server.course']"})
        },
        'Server.comment': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'comment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Server.course']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Server.place']", 'null': 'True'}),
            'sendername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'Server.course': {
            'Coursetype': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'Meta': {'object_name': 'course', 'db_table': "'server_course'"},
            'SchoolCode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'classnum': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'cname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'course_category': ('django.db.models.fields.IntegerField', [], {}),
            'courseid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'credit': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'day1': ('django.db.models.fields.IntegerField', [], {}),
            'day2': ('django.db.models.fields.IntegerField', [], {}),
            'day3': ('django.db.models.fields.IntegerField', [], {}),
            'day4': ('django.db.models.fields.IntegerField', [], {}),
            'day5': ('django.db.models.fields.IntegerField', [], {}),
            'day6': ('django.db.models.fields.IntegerField', [], {}),
            'day7': ('django.db.models.fields.IntegerField', [], {}),
            'ename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'manager': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Server.place']", 'null': 'True'}),
            'rawplace': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'teacherid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Server.teacher']", 'null': 'True'}),
            'teachername': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'termnumber': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time_test': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True'}),
            'txType': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'Server.notice': {
            'Meta': {'object_name': 'notice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ntype': ('django.db.models.fields.IntegerField', [], {}),
            'obj_id': ('django.db.models.fields.IntegerField', [], {}),
            'sendername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'touser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'Server.place': {
            'Meta': {'object_name': 'place'},
            'feedback': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'feedbacktime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'interid': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'keyid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rcapacity': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'roomtype': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'})
        },
        'Server.placet': {
            'Meta': {'object_name': 'placet'},
            'day1': ('django.db.models.fields.IntegerField', [], {}),
            'day2': ('django.db.models.fields.IntegerField', [], {}),
            'day3': ('django.db.models.fields.IntegerField', [], {}),
            'day4': ('django.db.models.fields.IntegerField', [], {}),
            'day5': ('django.db.models.fields.IntegerField', [], {}),
            'day6': ('django.db.models.fields.IntegerField', [], {}),
            'day7': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Server.place']"}),
            'weeknumber': ('django.db.models.fields.IntegerField', [], {})
        },
        'Server.profile': {
            'Meta': {'object_name': 'Profile'},
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mphone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'teach_courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Server.course']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'user_type': ('django.db.models.fields.IntegerField', [], {})
        },
        'Server.reply': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'reply'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sendername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sendfrom': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replys'", 'to': "orm['auth.User']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tocomment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Server.comment']"}),
            'toreply': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'touser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'Server.school': {
            'Meta': {'object_name': 'School'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'ename': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        'Server.sms': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'sms'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sendername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sendfrom': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sentsms'", 'to': "orm['auth.User']"}),
            'state': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'touser': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'inbox'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'Server.sys_notice': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'sys_notice'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sendername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'Server.teacher': {
            'Meta': {'object_name': 'teacher'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Server']