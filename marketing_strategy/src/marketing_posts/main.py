#!/usr/bin/env python
import sys
from marketing_posts.crew import MarketingPostsCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    '''
    inputs = {
        'customer_domain': 'crewai.com',
        'project_description': """
CrewAI, a leading provider of multi-agent systems, aims to revolutionize marketing automation for its enterprise clients. This project involves developing an innovative marketing strategy to showcase CrewAI's advanced AI-driven solutions, emphasizing ease of use, scalability, and integration capabilities. The campaign will target tech-savvy decision-makers in medium to large enterprises, highlighting success stories and the transformative potential of CrewAI's platform.

Customer Domain: AI and Automation Solutions
Project Overview: Creating a comprehensive marketing campaign to boost awareness and adoption of CrewAI's services among enterprise clients.
"""
    }
    '''
    inputs = {
        'customer_domain': 'https://www.philips.co.in/c-m-pe/oneblade-trim-edge-and-shave',
        'project_description': """
    Philips, a leading provider of Personal Care products, aims to revolutionize marketing automation for its consumers. This project involves developing an innovative marketing strategy to showcase Philips's advanced OneBlade product family, emphasizing ease of use, efficiency and comfort, dual protection and skincare. The campaign will target modern tech-savvy consumers, especially millenials, across geographies, highlighting comfort and style of this product.

    Customer Domain: Personal Care Products
    Project Overview: Creating a comprehensive marketing campaign to boost awareness and adoption of Philip's OneBlade product famiy among global consumers, especially targetting millenials.
    """
    }
    MarketingPostsCrew().crew().kickoff(inputs=inputs)


def train():
    # Train the crew for a given number of iterations.
    '''
    inputs = {
        'customer_domain': 'crewai.com',
        'project_description': """
CrewAI, a leading provider of multi-agent systems, aims to revolutionize marketing automation for its enterprise clients. This project involves developing an innovative marketing strategy to showcase CrewAI's advanced AI-driven solutions, emphasizing ease of use, scalability, and integration capabilities. The campaign will target tech-savvy decision-makers in medium to large enterprises, highlighting success stories and the transformative potential of CrewAI's platform.

Customer Domain: AI and Automation Solutions
Project Overview: Creating a comprehensive marketing campaign to boost awareness and adoption of CrewAI's services among enterprise clients.
"""
    }
    '''
    inputs = {
            'customer_domain': 'https://www.philips.co.in/c-m-pe/oneblade-trim-edge-and-shave',
            'project_description': """
        Philips, a leading provider of Personal Care products, aims to revolutionize marketing automation for its consumers. This project involves developing an innovative marketing strategy to showcase Philips's advanced OneBlade product family, emphasizing ease of use, efficiency and comfort, dual protection and skincare. The campaign will target modern tech-savvy consumers, especially millenials, across geographies, highlighting comfort and style of this product.

        Customer Domain: Personal Care Products
        Project Overview: Creating a comprehensive marketing campaign to boost awareness and adoption of Philip's OneBlade product famiy among global consumers, especially targetting millenials.
        """
        }
    try:
        MarketingPostsCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
