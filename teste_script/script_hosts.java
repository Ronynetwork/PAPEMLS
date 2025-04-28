double d = 1.1;
float f = 2.2f;
BigDecimal bd1 = new BigDecimal(d);    // 🚨 Noncompliant
BigDecimal bd2 = new BigDecimal(1.1);  // 🚨 Noncompliant
BigDecimal bd3 = new BigDecimal(f);    // 🚨 Noncompliant
