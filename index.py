from flask import Flask , render_template , request
app= Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/ports', methods=["GET","POST"])
def ports():
    import portScan
    from portScan import portScanner2
    ip=request.form['ipaddress']
    res=portScanner2(ip)
    return render_template("port.html", len=len(res) , pO=res)

@app.route('/xss', methods=["GET","POST"])    
def xss():
    import xssscan
    from xssscan import check_xss
    url=request.form['ipaddress']
    result=check_xss(url)
    return render_template("xss_scn.html",le=len(result),ur=url,p=result)

@app.route('/subdomain', methods=["GET","POST"])    
def subdomain():
    import subdomain
    from subdomain import subfinder
    url=request.form['ipaddress']
    result=subfinder(url)
    return render_template("subdomain.html",le=len(result),sublist=result)

@app.route('/sql', methods=["GET","POST"])    
def sql():
    import sql
    from sql import scan_sql_injection
    url=request.form['ipaddress']
    result=scan_sql_injection(url)
    return render_template("sql.html",le=len(result),sublist=result)

@app.route('/discover', methods=["GET","POST"])    
def discover():
    import filePathTraveral
    from filePathTraveral import content_discovery
    domain=request.form['ipaddress']
    result=content_discovery(domain)
    return render_template("filePathTraversal.html",le=len(result),sublist=result)


app.run(debug= True)
