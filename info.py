token = "5655731349:AAHpSNsDXkUochVg7jtVNeFadDa2JeA9-jE"
id = "5521639964"


x = [['09.11.2022', 'Aarhus', '3', 'Aarhus', '1900', '3', '0', '25', '19', '25', '23', '25', '19', 'W'],['04.03.', '20:00', 'Friedrichshafen', 'Luneburg', '1', '3', '23', '25', '25', '22', '21', '25', '18', '25', 'L'],['15.02.', '20:00', 'Friedrichshafen', 'Tours', '3', '2', '21', '25', '15', '25', '25', '18', '25', '21', '15', '11', 'W']]

line = list()


for i in x:

    one_line = list()
    for j in reversed(i):

        if j.isdigit():
            if int(j) not in [0,1,2,3]:
                one_line.append(int(j))

            if int(j) in [0,1,2,3]:
                print()
                break
    line.append(one_line)

    # print(line)



print(line)