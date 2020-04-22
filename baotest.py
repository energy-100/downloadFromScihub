from crossref.restful import Works

works = Works()
title="Quantum mechanics and hidden variables: A test of Bell's inequality by the measurement of the spin correlation in low-energy proton-proton scattering"
# w1 = works.query(title=title)
w1 = works.query(bibliographic=title)

# print(works.doi('10.1590/0102-311x00133115'))
# w1 = works.query(title='zika', author='johannes', publisher_name='Wiley-Blackwell')
for item in w1:
    print(item['title'])