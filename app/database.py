from models import Professor
for prof in Professor.objects():
	if prof.rank == 'ostadYar':
		prof.rank = u'استاد‌یار'
	if prof.rank == 'daneshYar':
		prof.rank = u'دانش‌یار'
	if prof.rank == 'ostad tamam':
		prof.rank = u'استاد تمام'
	if prof.rank == 'ostad madov':
		prof.rank = u'استاد مدعو'
	if prof.rank == 'bazneshaste':
		prof.rank = u'بازنشسته'
	if prof.rank == 'sayer':
		prof.rank = u'سایر'
	prof.save()
	
		