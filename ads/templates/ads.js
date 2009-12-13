gp_ads = Array({}
{% for ad in ads %}
, {'id': '{{ad.id}}',
'name': '{{ad.name}}',
'weight': '{{ad.weight}}',
'url': '{{ad.url}}',
'text': '{{ad.html}}',
'image': '{{ad.image}}'}
{% endfor %});
gp_ads.shift();
function gp_pick_ad() {
    el = Math.floor ( Math.random() * gp_ads.length) ;
    ad = gp_ads[el];
    ad_html = '<a href="' + ad.url + '"><img src="http://www.ftrain.com/media/'+ad.image+'"></a><a id="gp_body" href="'+ad.url+'">'+ad.text+'</a><a id="gp_tag" href="http://www.gratefulpublic.com">ad: <b>[grateful public]</b></a>';
    return ad_html;
}
