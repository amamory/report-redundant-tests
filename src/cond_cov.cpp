
int Condition_Cov(bool a,bool b,bool c)
{
    // non-sense logic just to test condition coverage
    if ((a || b) && c)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

