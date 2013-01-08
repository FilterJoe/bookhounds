# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Publisher'
        db.create_table('books_publisher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('state_province', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('books', ['Publisher'])

        # Adding model 'Author'
        db.create_table('books_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('Amazon_author_link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('books', ['Author'])

        # Adding model 'Book'
        db.create_table('books_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='books', to=orm['books.Publisher'])),
            ('publication_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('ISBN13', self.gf('django.db.models.fields.CharField')(unique=True, max_length=14)),
            ('Amazon_book_link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('Amazon_book_data', self.gf('django.db.models.fields.TextField')(max_length=400, null=True, blank=True)),
            ('image_URL', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('books', ['Book'])

        # Adding M2M table for field authors on 'Book'
        db.create_table('books_book_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['books.book'], null=False)),
            ('author', models.ForeignKey(orm['books.author'], null=False))
        ))
        db.create_unique('books_book_authors', ['book_id', 'author_id'])

        # Adding model 'AuthorList'
        db.create_table('books_authorlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('short_description', self.gf('django.db.models.fields.TextField')(max_length=256, null=True, blank=True)),
            ('long_description', self.gf('django.db.models.fields.TextField')(max_length=4096, null=True, blank=True)),
            ('creator_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('books', ['AuthorList'])

        # Adding model 'AuthorInclusion'
        db.create_table('books_authorinclusion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Author'])),
            ('author_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.AuthorList'])),
            ('rank', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('inclusion_reason', self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True)),
        ))
        db.send_create_signal('books', ['AuthorInclusion'])

        # Adding model 'BookList'
        db.create_table('books_booklist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('short_description', self.gf('django.db.models.fields.TextField')(max_length=256, null=True, blank=True)),
            ('long_description', self.gf('django.db.models.fields.TextField')(max_length=4096, null=True, blank=True)),
            ('creator_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('books', ['BookList'])

        # Adding model 'BookInclusion'
        db.create_table('books_bookinclusion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Book'])),
            ('book_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.BookList'])),
            ('rank', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('inclusion_reason', self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True)),
        ))
        db.send_create_signal('books', ['BookInclusion'])


    def backwards(self, orm):
        # Deleting model 'Publisher'
        db.delete_table('books_publisher')

        # Deleting model 'Author'
        db.delete_table('books_author')

        # Deleting model 'Book'
        db.delete_table('books_book')

        # Removing M2M table for field authors on 'Book'
        db.delete_table('books_book_authors')

        # Deleting model 'AuthorList'
        db.delete_table('books_authorlist')

        # Deleting model 'AuthorInclusion'
        db.delete_table('books_authorinclusion')

        # Deleting model 'BookList'
        db.delete_table('books_booklist')

        # Deleting model 'BookInclusion'
        db.delete_table('books_bookinclusion')


    models = {
        'books.author': {
            'Amazon_author_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Author'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        'books.authorinclusion': {
            'Meta': {'ordering': "('rank',)", 'object_name': 'AuthorInclusion'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['books.Author']"}),
            'author_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['books.AuthorList']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion_reason': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'books.authorlist': {
            'Meta': {'object_name': 'AuthorList'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'author_lists'", 'symmetrical': 'False', 'through': "orm['books.AuthorInclusion']", 'to': "orm['books.Author']"}),
            'creator_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'books.book': {
            'Amazon_book_data': ('django.db.models.fields.TextField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'Amazon_book_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ISBN13': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '14'}),
            'Meta': {'object_name': 'Book'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'books'", 'symmetrical': 'False', 'to': "orm['books.Author']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_URL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'books'", 'to': "orm['books.Publisher']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'books.bookinclusion': {
            'Meta': {'ordering': "('rank',)", 'object_name': 'BookInclusion'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['books.Book']"}),
            'book_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['books.BookList']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion_reason': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'books.booklist': {
            'Meta': {'object_name': 'BookList'},
            'books': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'book_lists'", 'symmetrical': 'False', 'through': "orm['books.BookInclusion']", 'to': "orm['books.Book']"}),
            'creator_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'books.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['books']