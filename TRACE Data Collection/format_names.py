marketing = ['Yakov Bart', 'Kwong Chan', 'Angela Chang', 'Bruce Clark', 'Alexander DePaoli', 'Paul W. Fombelle', 'Sean M. Gallagher', 'Myles Garvey', 'Nabeel Gillani', 'Amir Grinstein', 'Brooke Johnson', 'Yael Karlinsky Shichor', 'Ashley Keeney', 'Samsun Knight', 'Smriti Kumar', 'Didem Kurt', 'Felicia Lassk', 'Shun-Yang Lee', 'Duane Lefevre', 'Ted Matherly', 'Daniele Mathras', 'Ernest Mauristhene', 'Robert McCullough', 'Jay Mulki', "Chad O'Connor", 'Koen Pauwels', 'Amy Pei', 'Ron Rivas', 'Matt Rocklage', 'Julian Runge', 'Erica Sands', 'Jeffrey Sieloff', 'Mary Steffel', 'Rachel Stewart', 'Fareena Sultan', 'Sharon Thomas', 'Ray Weaver', 'Dena Yadin', 'Jennifer Yencho', 'Yi Yin']
accounting = ["Udi Hoitash","Gayathri Nataraja","Mario Maletta","Kimberly Moreno","Majorie Platt","Tim Rupert","H Sherman","Xiaoto Liu","Yang Zhang","Jiyoun Ahn","Evisa Bogdani","Mary Dodgson","Hetrick Kamber","Patrick Hurley","Shuyang Wang","Xia Xiao"]
eANDi = ["Kimberly Eddleston","Stine Grodal","Samina Karim","Ralph Katz","Marc Meyer","Fernando Suarez","Tucker Marion","Kevin Boudreau","Melvin Kelley","Razvan Lungeanu","Venkat Kuppuswamy","Kinde Wubneh"]
finance = ["Rajesh Aggarwal","Jeffery Born","Nicole Boyson","Olubunmi Faleye","Robert Mooradian","Harlan Platt","Emery Trahan","Jianqiu Bai","Tiantian Gu","Karthik Krishnan","Anand Venkateswaran","Shiawee Yang","Kuncheng Zheng","Weiling Liu","Sanjeev Mukerjee","Andres Shahidinejad","Ali Sharifkhani","Fabricius Somogyi","Kandarp Srinivasan"]
ibs = ["Ruth Aguilera","Paula Caligiuri","Hugh Courtney","William Crittenden","Alvaro Cuervo-Cazurra","James Dana","Mark Huselid","Sheila Puffer","Ravi Ramamurti","Christopher Robertson","Ravi Sarathy","Gary Young","Todd Aleessandri","Elitsa Banalieva","Luis Dau","Anna Lamin","Valentina Marano","Bert Spector","C Un","Kevin Chuah"]
scim = ["Nada R. Sanders","Cuneyt Eroglu","Yang W. Lee","Gilbert Nyaga","Christoph Riedl","Shawn Bhimani","John Lowery"]
mod = ["John Dencker","Timothy Hoff","Laura Huang","Cynthia Lee","Lua Kamál Yuille","Marla Baskerville","Jamie J. Ladge","Edward G. Wertheim","Zhenyu Liao","Manuel Vaulont"]

def reverse(list):
    reversed = []
    for i in list:
        split = i.replace(',', '').split(' ')
        reversed.append(', '.join(split[::-1]))
    print(reversed)
    print([i.replace(' ', ', ') for i in list])
    return(reversed)
reverse(marketing)
        