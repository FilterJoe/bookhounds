# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Publisher.name'
        db.alter_column('books_publisher', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

    def backwards(self, orm):

        # Changing field 'Publisher.name'
        db.alter_column('books_publisher', 'name', self.gf('django.db.models.fields.CharField')(max_length=30))

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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['books']