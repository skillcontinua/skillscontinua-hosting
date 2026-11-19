# File path: C:\hosting\skillscontinua_hosting\village\translation.py
from modeltranslation.translator import translator, TranslationOptions
from .models import MonetizationOffer, CommunityPost, ForumTopic, MediaStream, SocialChannel


class MonetizationOfferTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'call_to_action_text', 'price_display')


class CommunityPostTranslationOptions(TranslationOptions):
    fields = ('title', 'summary')


class ForumTopicTranslationOptions(TranslationOptions):
    fields = ('title', 'body')


class MediaStreamTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class SocialChannelTranslationOptions(TranslationOptions):
    fields = ('handle_or_label', 'follower_count_label')


translator.register(MonetizationOffer, MonetizationOfferTranslationOptions)
translator.register(CommunityPost, CommunityPostTranslationOptions)
translator.register(ForumTopic, ForumTopicTranslationOptions)
translator.register(MediaStream, MediaStreamTranslationOptions)
translator.register(SocialChannel, SocialChannelTranslationOptions)